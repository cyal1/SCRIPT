# loader.py
import time
import frida
import requests


def my_message_handler(message, payload):
    print(message)
    print(payload)

# device = frida.get_usb_device()
device = frida.get_device_manager().add_remote_device('127.0.0.1:27042')
# pid = device.spawn(["com.yuanrenxue.match2022"])
# device.resume(pid)
# time.sleep(5)  # Without it Java.perform silently fails
session = device.attach(11076)
with open("python_to_call_function.js") as f:
    script = session.create_script(f.read())
script.on("message", my_message_handler)
script.load()

command = ""

sum = 0
for page in range(1, 101):
    timestamp = str(time.time()).split(".")[0]
    encrypt_text = script.exports.callencryptfunction('page=' + str(page) + timestamp)
    resp = requests.post("https://appmatch.yuanrenxue.com/app1", data={
        "page": str(page),
        "sign": encrypt_text,
        "t": timestamp,
        "token": "0ZIAcmjVUjXfYBMKeg81DhPCRNYwvM%2FMpRIw%2FAJKW03jiPEzX4uSAgROhDdd2Wh2"
    })
    print(page, resp.json())
    for i in resp.json()["data"]:
        sum += int(i["value"].strip())
print(sum)


# while 1 == 1:
#     command = raw_input("Enter command:\n1: Exit\n2: Call secret function\n3: Hook Secret\nchoice:")
#     if command == "1":
#         break
#     elif command == "2":
#         script.exports.callencryptfunction()
#     elif command == "3":
#         script.exports.hookencryptfunction()