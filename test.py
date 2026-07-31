import subprocess
import time

while True:
    result = subprocess.run(
        ["mpremote", "connect", "auto", "exec", "print('OK')"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Device connected")
        break
    else:
        time.sleep(0.5)