import argparse
import os
import socket
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from schedule_vol import get_now, Volumizer

app = Flask(__name__)
scheduler = None


class Globals:
    def __init__(self):
        self.v = Volumizer()
        self.scheduler = None
        self.stop_ramp = False


_g = Globals()

####################################################
# Heper functions
####################################################


def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    s.close()
    return ip

def try_report_ip():
    ip = myip()
    print(f"IP is {ip}")
    url = 'http://ec3.sfflux.com/djoli/postip'
    myobj = {'ip': str(ip)}
    try:
        x = requests.post(url, json = myobj, timeout=5)
        print(f"Reported IP result {x}")
    except Exeption as ex:
        print("Failed to report ip: {ex}")
        return


def _serve_file(fid):
    pth = f"./files/{fid}"
    if not os.path.exists(pth):
        raise Exception(f"Path not found: {pth}")
    mode = "r"
    if "png" in fid or "ico" in fid:
        mode = "rb"
    with open(pth, mode) as f:
        return f.read()


####################################################
# Routes
####################################################


def _cmd_resp(c):
    return {"res": "OK", "command": c, "time": get_now()}


@app.route("/vol/off")
def vol_off():
    global _g
    print("vol off")
    _g.v.apply_boost(b_abs=-10)
    return _cmd_resp("vol_off")


@app.route("/vol/less")
def vol_less():
    global _g
    _g.v.apply_boost(b_delta=-1)
    print("vol less")
    return _cmd_resp("vol_less")


@app.route("/vol/more")
def vol_more():
    global _g
    _g.v.apply_boost(b_delta=1)
    print("vol more")
    return _cmd_resp("vol_more")


@app.route("/vol/max")
def vol_max():
    global _g
    _g.v.apply_boost(b_abs=7)
    print("vol max")
    return _cmd_resp("vol_max")


##################################################
# Ramps
##################################################


def do_ramp(delta):
    print(f"Background job doing ramp {delta}")
    ramp_intervals = int(10 * abs(delta))
    ramp_seconds = int(5 * abs(delta))
    for i in range(ramp_intervals):
        if _g.stop_ramp:
            _g.stop_ramp = False
            print("Stopping ramp")
            return
        _g.v.apply_boost(b_delta=(delta / ramp_intervals))
        time.sleep(ramp_seconds / ramp_intervals)


@app.route("/vol/rampup")
def ramp_up():
    global _g
    print("ramp up")
    _g.scheduler.add_job(
        do_ramp, "date", run_date=datetime.now() + timedelta(seconds=1), args=[1.0]
    )
    return _cmd_resp("rampup")


@app.route("/vol/rampdown")
def ramp_down():
    global _g
    _g.scheduler.add_job(
        do_ramp, "date", run_date=datetime.now() + timedelta(seconds=1), args=[-1.0]
    )
    print("ramp down")
    return _cmd_resp("ramp_down")


@app.route("/vol/rampmax")
def ramp_max():
    global _g
    print("ramp_max")
    _g.scheduler.add_job(
        do_ramp, "date", run_date=datetime.now() + timedelta(seconds=1), args=[7.0]
    )
    return _cmd_resp("ramp_max")


@app.route("/vol/rampoff")
def ramp_off():
    global _g
    _g.scheduler.add_job(
        do_ramp, "date", run_date=datetime.now() + timedelta(seconds=1), args=[-10.0]
    )
    print("ramp off")
    return _cmd_resp("ramp_off")


@app.route("/vol/unset")
def vol_unset():
    global _g
    _g.stop_ramp = True
    _g.v.apply_boost(b_abs=0.0)
    print("vol boost unset")
    return _cmd_resp("vol_unset")


@app.route("/status")
def status():
    global _g
    now = get_now()
    vol = _g.v.get_vol(now)
    return {
        "boost": round(_g.v.boost, 2),
        "updated_at": _g.v.updated_at,
        "vol": round(vol, 2),
        "now": now,
    }


@app.route("/files/<fid>")
def get_files(fid):
    return _serve_file(fid)


@app.route("/index.html")
def get_index(fid):
    return _serve_file("index.html")


@app.route("/")
def homepage():
    return _serve_file("index.html")


####################################################
# Main
####################################################


def background_job():
    global _g

    _g.v.update()

    try_report_ip()


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

    try_report_ip()

    # run once immediately on init
    background_job()

    print("Starting background scheduler")
    _g.scheduler = BackgroundScheduler()
    job = _g.scheduler.add_job(background_job, "interval", minutes=5)
    _g.scheduler.start()

    # app.run(debug=args.debug_mode, host="127.0.0.1", port=80)
    app.run(debug=args.debug_mode, host="0.0.0.0", port=8080)
