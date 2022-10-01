from flask import Flask, render_template
from threading import Thread
import bot

app = Flask(__name__, template_folder="./template")

@app.route("/")
def home():
    log_file = open("./data/logs.txt")
    logs = [log for log in log_file]
    logs = logs[::-1]
    return render_template("log.html", logs= logs)


def keep_alive():
    app.run(host="0.0.0.0", port=8080)

def start():
    t1 = Thread(target=keep_alive)
    t1.start()

if __name__ == "__main__":
    bot.start_bot()
    app.run(host="0.0.0.0", port=8080, debug=True)
