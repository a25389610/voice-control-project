from flask import Flask, request
import RPi.GPIO as GPIO
import time
import threading
from tm1637 import TM1637

app = Flask(__name__)

# 設定 GPIO 腳位
LED_PIN = 17
SERVO_PIN = 18
BUZZER_PIN = 27
DISPLAY_CLK = 21
DISPLAY_DIO = 20

servo_pwm = None
stereo_thread = None
stereo_active = False

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 初始化蜂鳴器
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 440)
buzzer_pwm.start(0)

# 初始化七段顯示器
display = TM1637(clk=DISPLAY_CLK, dio=DISPLAY_DIO)
display.brightness(1)

# 星際大戰旋律
star_wars_notes = [
    (440, 0.5), (440, 0.5), (440, 0.5),
    (349, 0.35), (523, 0.15),
    (440, 0.5), (349, 0.35), (523, 0.15), (440, 1.0),
    (659, 0.5), (659, 0.5), (659, 0.5),
    (698, 0.35), (523, 0.15),
    (415, 0.5), (349, 0.35), (523, 0.15), (440, 1.0),
]

def play_star_wars():
    global stereo_active
    while stereo_active:
        for freq, duration in star_wars_notes:
            if not stereo_active:
                break
            buzzer_pwm.ChangeFrequency(freq)
            buzzer_pwm.ChangeDutyCycle(50)
            time.sleep(duration)
            buzzer_pwm.ChangeDutyCycle(0)
            time.sleep(0.05)
        time.sleep(0.5)

@app.route('/voice', methods=['POST'])
def receive_voice():
    global servo_pwm, stereo_thread, stereo_active
    data = request.get_json()
    command = data.get("text", "").lower()
    print("Received voice command:", command)

    # 開燈 / 關燈
    if command == "turn on the light":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("Action: Turn on the light")
    elif command in ["turn off the light", "turn off the lights"]:
        GPIO.output(LED_PIN, GPIO.LOW)
        print("Action: Turn off the light")

    # 冷氣（伺服馬達控制）
    elif command == "open the air conditioner":
        if servo_pwm is None:
            servo_pwm = GPIO.PWM(SERVO_PIN, 50)
            servo_pwm.start(6.5)
        else:
            servo_pwm.ChangeDutyCycle(6.5)
        print("Action: Air conditioner ON (fan spinning)")
    elif command == "turn off the air conditioner":
        if servo_pwm:
            servo_pwm.ChangeDutyCycle(7.0)
            time.sleep(0.3)
            servo_pwm.ChangeDutyCycle(0)
        print("Action: Air conditioner OFF (fan stopped)")

    # 音響（蜂鳴器）
    elif command == "open the stereo":
        if not stereo_active:
            stereo_active = True
            stereo_thread = threading.Thread(target=play_star_wars)
            stereo_thread.start()
            print("Action: Playing Star Wars Theme")
    elif command == "turn off the stereo":
        stereo_active = False
        buzzer_pwm.ChangeDutyCycle(0)
        print("Action: Stereo OFF")

    # 電視（七段顯示器）
    elif command == "open the tv":
        display.show(' ON ')
        print("Action: TV ON")
    elif command == "turn off the tv":
        display.show('OFF')
        print("Action: TV OFF")

    return {"status": "ok", "received": command}

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        stereo_active = False
        if stereo_thread:
            stereo_thread.join()
        if servo_pwm:
            servo_pwm.stop()
        buzzer_pwm.stop()
        display.write([0, 0, 0, 0])  # 清除顯示
        GPIO.cleanup()
