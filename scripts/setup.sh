arduino --upload ~/Arduino/light_telemetry_module/telemetry_module.ino --port /dev/ttyUSB1
arduino --upload ~/Arduino/telemetry_module/light_telemetry_module.ino --port /dev/ttyUSB0
arduino --upload ~/Arduino/irrigation_module/irrigation_module.ino --port /dev/ttyACM0
python main.py