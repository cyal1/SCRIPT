# loader.py
import time
import frida
import requests


def my_message_handler(message, payload):
    print(message)
    print(payload)

    if message["type"] == "send":

        data = message["payload"]
        # handle data
        script.post({"python_data": data})  # send JSON object


device = frida.get_device_manager().add_remote_device('127.0.0.1:27042')

pid = device.spawn(["com.yuanrenxue.match2022"])

device.resume(pid)

time.sleep(1)

session = device.attach(pid)

with open("modify_params.js") as f:
    script = session.create_script(f.read())
script.on("message", my_message_handler)  # register the message handler
script.load()
input()