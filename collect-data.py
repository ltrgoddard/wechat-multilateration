#!/usr/bin/env python3
import frida, sys, json, random, time, os

RUNS = int(sys.argv[1])
COORDS = list(map(lambda x: float(x), sys.argv[2].split(",")))
MESSAGES = []
LAT = 0
LON = 0

def on_message(message, data):
  global LAT, LON, MESSAGES

  if "payload" in message.keys():
    MESSAGES.append(message["payload"])
    i = len(MESSAGES) - 2

    if MESSAGES[i + 1][0:6] == "Within":
      print(json.dumps({
        "user": MESSAGES[i],
        "dist": int(
          MESSAGES[i + 1] \
            .replace("Within", "") \
            .replace("km", "000") \
            .replace("m", "")),
        "lat": LAT,
        "lon": LON
      }))
      sys.stdout.flush()

device = frida.get_usb_device()

for run in range(RUNS):
  pid = device.spawn(["com.tencent.mm"])
  session = device.attach(pid)

  LON = random.uniform(COORDS[0], COORDS[2])
  LAT = random.uniform(COORDS[1], COORDS[3])
  
  hook = f"""
    Java.perform(function() {{
      const Location = Java.use("android.location.Location");
      const TextView = Java.use("android.widget.TextView");

      // Make mocked locations look real to WeChat
      Location.isFromMockProvider.implementation = function() {{
        return false;
      }}

      // Return mock longitude
      Location.getLongitude.implementation = function() {{
        return {str(LON)};
      }}

      // Return mock latitude
      Location.getLatitude.implementation = function() {{
        return {str(LAT)};
      }}

      // Forward all displayed text to Python
      TextView.setText.overload("java.lang.CharSequence").implementation = function(text) {{
        send(text.toString());
        return this.setText(text);
      }}
    }})
  """
  script = session.create_script(hook)
  script.on("message", on_message)
  script.load()
  
  device.resume(pid)
  time.sleep(6)
  # Input coordinates are for a Gooogle Pixel 4a -
  # adjust for other devices
  os.system("adb shell input tap 700 2200")
  time.sleep(1)
  os.system("adb shell input tap 500 1000")
  time.sleep(7)
  for i in range(4):
    os.system("adb shell input swipe 500 2200 500 0")
    time.sleep(.5)
