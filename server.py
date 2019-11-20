from flask import Flask, request
import time

app = Flask(__name__)
messages=[
    {"username": "Tim", "time": time.time(), "text":"Hello!"},
    {"username": "Mary", "time": time.time(), "text":"Hi!"}
]

password_storage = {
    "Tim": "sdfgsdf",
    "Mary": "4444"
}

@app.route("/")
def status_method():
    return "Current time on server " + str(time.time())

@app.route("/send", methods=["POST"])
def send_method():
    """
    JSON {username: str, text: str}
    :return:
    """
    password = request.json["password"]
    username = request.json["username"]
    text = request.json["text"]

    #first attempt for user
    if username not in password_storage:
        password_storage[username] = password

    #validate
    if not isinstance(username, str) or len(username) == 0:
        return {"ok":False}
    if not isinstance(text, str) or len(text) == 0:
        return {"ok":False}
    if password_storage[username] != password:
        return {"ok":False}

    messages.append({"username": username, "time": time.time(), "text":text})
    return {"ok":True}

@app.route("/messages")
def messages_method():
    """
    Param after - мекто времени, после которй получаем сообщения
    :return: {"messages": [
        {usename: str, time: float, text:str}
        ...
    ]}
    """
    after = float(request.args["after"])
    messages_after = [message for message in messages if message["time"] > after]
    return {"messages":messages_after}

app.run()