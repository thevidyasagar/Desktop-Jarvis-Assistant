import sounddevice as sd
try:
    print("Devices:", sd.query_devices())
    print("Default device:", sd.default.device)
except Exception as e:
    print("Error querying devices:", e)
