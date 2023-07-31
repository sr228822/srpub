import argparse
from dataclasses import dataclass
from flask import Flask
import socket
import time

import schedule_vol

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    s.close()

@dataclass
class Globals:
    boost = 0.0
    updated_at = None

_g = Globals()

####################################################
# Routes
####################################################

@app.route('/vol/off')
def vol_off():
    global _g
    print("vol off")
    _g.boost = -100
    _g.updated_at = time.time()
    return {'res': 'OK', 'command': 'vol_off'}

@app.route('/vol/less')
def vol_less():
    global _g
    _g.boost -= 1
    _g.updated_at = time.time()
    print("vol less")
    return {'res': 'OK', 'command': 'vol_less'}

@app.route('/vol/more')
def vol_more():
    global _g
    _g.boost += 1
    _g.updated_at = time.time()
    print("vol more")
    return {'res': 'OK', 'command': 'vol_more'}

@app.route('/vol/max')
def vol_max():
    global _g
    _g.boost = 100
    _g.updated_at = time.time()
    print("vol max")
    return {'res': 'OK', 'command': 'vol_max'}

@app.route('/status')
def status():
    global _g
    now = schedule_vol.get_now()
    vol = schedule_vol.get_vol(now)
    return {"boost": _g.boost, "updated_at": _g.udpated_at, "vol": vol, "now": now}


@app.route('/')
def homepage():
    return 'Hello, World!'

####################################################
# Main
####################################################

def test_job():
    global _g

    now = schedule_vol.get_now()
    vol = schedule_vol.get_vol(now)
    schedule_vol.print_status(now, vol)
    schedule_vol.set_vol(vol)

    print(f'i am test job. boost is {_g.boost}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        web-server example
"""
    )
    parser.add_argument(
        "--debug-mode",
        dest="debug_mode",
        action="store_true",
        help="Run in debug mode, where flask auto-restarts on code-changes",
    )
    args = parser.parse_args()

    myip()

    print("Starting background scheduler")
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(test_job, 'interval', minutes=0.1)
    scheduler.start()

    #app.run(debug=args.debug_mode, host="127.0.0.1", port=80)
    app.run(debug=args.debug_mode, host="0.0.0.0", port=8080)
