# Voice-Control Project

A voice-command IoT system that **simulates smart home appliance control** using **Flask backend** and **Raspberry Pi GPIO**.

This project allows users to **control devices using voice commands** via **Siri Shortcuts** on iPhone.  
The system simulates appliances like **lights, air conditioners, TVs, and speakers** using LEDs, servo motors, 7-segment displays, and buzzers.

---

##  Features

-  Voice control via Siri Shortcut (Chinese-to-English conversion)
-  Flask web server to receive and process commands
-  Real-time GPIO control on Raspberry Pi
-  LED to simulate lights
-  Servo motor to simulate an air conditioner
-  7-segment display to simulate TV ON/OFF
-  Buzzer to simulate speaker

---

##  Project Structure

voice-control-project/
──  server/
     ──  voice_server.py # Flask server handling voice commands
     ── tm1637.py # TM1637 display control module
──  images/
     ── DEMO.mp4 # Demo video of the project
── docs/
     ── 語音指令控制系統_期末.pdf # Final project report (Chinese)
── README.md


---

## System Flow

1. User speaks a command (e.g., "Turn on the light") into iPhone Siri
2. Siri Shortcut converts voice → English text → sends HTTP request to Flask server
3. Flask receives the command, processes it
4. Raspberry Pi triggers corresponding GPIO action (LED, motor, etc.)

---

##  Demo

 [Click to view demo](./images/DEMO.mp4)

---

##  Final Report

 [期末報告：語音指令控制系統](./docs/語音指令控制系統_期末.pdf)

---

##  Future Improvements

- Deploy server to cloud or local Wi-Fi network
- Add natural language understanding (e.g., "開電燈", "燈打開" 都能判斷)
- Expand device types or connect to real appliances (e.g., via IR or relay)
- Add voice response feedback

---

##  Author

Created by [a25389610](https://github.com/a25389610) as a university IoT project (2025).


