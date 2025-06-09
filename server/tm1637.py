
# tm1637.py 驅動程式 (支援 Raspberry Pi)
# 來源: github.com/dword1511/tm1637 的簡化版本

import RPi.GPIO as GPIO
import time

SEGMENTS = {
    ' ': 0x00,
    '-': 0x40,
    '0': 0x3f,
    '1': 0x06,
    '2': 0x5b,
    '3': 0x4f,
    '4': 0x66,
    '5': 0x6d,
    '6': 0x7d,
    '7': 0x07,
    '8': 0x7f,
    '9': 0x6f,
    'A': 0x77,
    'b': 0x7c,
    'C': 0x39,
    'd': 0x5e,
    'E': 0x79,
    'F': 0x71,
    'H': 0x76,
    'L': 0x38,
    'O': 0x3f,
    'P': 0x73,
    'U': 0x3e,
    'n': 0x54,
    'o': 0x5c,
    'r': 0x50,
    't': 0x78,
    'y': 0x6e,
    'N': 0x37,
    'f': 0x71,
}

class TM1637:
    def __init__(self, clk, dio, brightness=7):
        self.clk = clk
        self.dio = dio
        self.brightness = brightness & 0x07
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.dio, GPIO.OUT)
        self.clear()

    def start(self):
        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.output(self.dio, GPIO.HIGH)
        GPIO.output(self.dio, GPIO.LOW)
        GPIO.output(self.clk, GPIO.LOW)

    def stop(self):
        GPIO.output(self.clk, GPIO.LOW)
        GPIO.output(self.dio, GPIO.LOW)
        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.output(self.dio, GPIO.HIGH)

    def write_byte(self, data):
        for i in range(8):
            GPIO.output(self.clk, GPIO.LOW)
            GPIO.output(self.dio, (data >> i) & 1)
            GPIO.output(self.clk, GPIO.HIGH)
        GPIO.output(self.clk, GPIO.LOW)
        GPIO.setup(self.dio, GPIO.IN)
        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.setup(self.dio, GPIO.OUT)

    def set_brightness(self, brightness):
        self.brightness = brightness & 0x07

    def clear(self):
        self.show([' ', ' ', ' ', ' '])

    def show(self, data):
        segments = [SEGMENTS.get(x.upper(), 0x00) for x in data]
        self.start()
        self.write_byte(0x40)
        self.stop()
        self.start()
        self.write_byte(0xc0)
        for seg in segments:
            self.write_byte(seg)
        self.stop()
        self.start()
        self.write_byte(0x88 | self.brightness)
        self.stop()
