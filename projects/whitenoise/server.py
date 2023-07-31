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

class Globals:
    def __init__(self):
        self.v = schedule_vol.Volumizer()

_g = Globals()

####################################################
# Routes
####################################################

@app.route('/vol/off')
def vol_off():
    global _g
    print("vol off")
    _g.v.apply_boost(b_abs=-10)
    return {'res': 'OK', 'command': 'vol_off'}

@app.route('/vol/less')
def vol_less():
    global _g
    _g.v.apply_boost(b_delta=-1)
    print("vol less")
    return {'res': 'OK', 'command': 'vol_less'}

@app.route('/vol/more')
def vol_more():
    global _g
    _g.v.apply_boost(b_delta=1)
    print("vol more")
    return {'res': 'OK', 'command': 'vol_more'}

@app.route('/vol/max')
def vol_max():
    global _g
    _g.v.apply_boost(b_abs=7)
    print("vol max")
    return {'res': 'OK', 'command': 'vol_max'}

@app.route('/vol/unset')
def vol_unset():
    global _g
    _g.v.apply_boost(b_abs=0.0)
    print("vol boost unset")
    return {'res': 'OK', 'command': 'vol_unset'}

@app.route('/status')
def status():
    global _g
    now = schedule_vol.get_now()
    vol = _g.v.get_vol(now)
    return {"boost": round(_g.v.boost, 2), "updated_at": _g.v.updated_at, "vol": round(vol, 2), "now": now}


@app.route('/')
def homepage():
    return 'Hello, World!'

####################################################
# Main
####################################################

def background_job():
    global _g

    _g.v.update()

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

    # run once immediately on init
    background_job()

    print("Starting background scheduler")
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(background_job, 'interval', minutes=0.1)
    scheduler.start()

    #app.run(debug=args.debug_mode, host="127.0.0.1", port=80)
    app.run(debug=args.debug_mode, host="0.0.0.0", port=8080)
