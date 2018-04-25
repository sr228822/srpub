#! /usr/bin/env python

import subprocess, math, time, sys, datetime, commands, re

def ash(c, wait=True, noisy=False):
    fullcmd = 'adb shell "' + c + '"'
    return cmd(fullcmd, wait=wait, noisy=noisy)

def getprop(prop):
    return ash('getprop ' + prop, wait=True, noisy=False)

def adb_available():
    res = cmd('adb get-state')
    return 'device' in res.lower()

def utc_seconds():
    import calendar
    return calendar.timegm(time.gmtime())

def noisy_sleep(duration, tag=''):
    start = datetime.datetime.now()
    while True:
        time.sleep(1)
        left = duration - seconds_between(start, datetime.datetime.now())
        if left <= 0:
            break
        hrs = int(left / 3600)
        mins = int((left / 60) % 60)
        secs = left % 60
        flushprint(tag + ' ' + '%02d' % hrs + ':' + '%02d' % mins + ':' + '%02d' % secs)
        if int(secs) % 10 == 0:
            try:
                import alice
                if alice.alice_enabled():
                    alice.alice_check_status()
            except:
                pass
    flushprint('                                                ')
    print ''

def flushprint(l):
    sys.stdout.write("\r" + str(l) + "                   ")
    sys.stdout.flush()

def flushprint_to_stderr(l, nobuffer=False):
    if nobuffer:
        sys.stderr.write("\r" + str(l))
    else:
        sys.stderr.write("\r" + str(l) + "                   ")
    sys.stderr.flush()

def status_bar(done, total, width=40):
    perc = int(width * float(done) / float(total))
    flushprint('[' + '|' * perc + ' ' * (width-perc) + ']')

def print_to_stderr(p):
    sys.stderr.write(p + '\n')

def in_tmux():
    #r = cmd('echo $TERM')
    r = cmd('echo $TMUX')
    return r != ''

def quick_ingest_line():
    while True:
        line = sys.stdin.readline()
        if not line:
            return
        yield line

def is_uuid(s):
    import uuid
    try:
        uuid.UUID(s)
        return True
    except:
        return False

def is_email(s):
    return '@' in s

#################################################################
# Internet Reading
#################################################################

def html_read_timeout(url, to):
    try:
        import urllib2
        req = urllib2.Request(url)
        #print '{url',
        resp = urllib2.urlopen(req, timeout=to)
        #print ' success}'
        return resp.read()
    except:
        print '{url fail}'
        return ''

def html_read(url):
    return html_read_timeout(url, 20)

#################################################################
# Pickling to/from files
#################################################################
def load_pickle(fname):
    import pickle
    with open(fname, 'rb') as f:
        result = pickle.load(f)
    return result

def save_pickle(obj, fname):
    import pickle
    with open(fname, 'wb') as f:
        pickle.dump(obj, f)

#################################################################
# Time
#################################################################

def date_to_str(d):
    return d.strftime("%Y.%m.%d.%H.%M.%S")

def str_to_date(s):
    return datetime.datetime.strptime(s, "%Y.%m.%d.%H.%M.%S")

def get_now():
    return datetime.datetime.now()

def seconds_between(da, db):
    return (db - da).total_seconds()

def hours_between(da, db):
    return seconds_between(da, db) / 3600

def parse_duration(txt):
    duration = txt
    if 'm' in duration:
        duration = re.sub('m', '', duration)
        duration = 60 * float(duration)
    elif 'h' in duration:
        duration = re.sub('h', '', duration)
        duration = 60 * 60 * float(duration)
    elif 'd' in duration:
        duration = re.sub('d', '', duration)
        duration = 24 * 60 * 60 * float(duration)
    else:
        duration = re.sub('s', '', duration)
        duration = int(duration)
    return duration

#################################################################
# Coloring
#################################################################

def termcode(num):
    return '\033[%sm'%num

def brilliant_str(txt):
    return bold_str(termcode(41) + txt + termcode(0))
def red_str(txt):
    return termcode(91) + txt + termcode(0)
def green_str(txt):
    return termcode(32) + txt + termcode(0)
def yellow_str(txt):
    return termcode(93) + txt + termcode(0)
def blue_str(txt):
    return termcode(34) + txt + termcode(0)
def magenta_str(txt):
    return termcode(35) + txt + termcode(0)
def grey_str(txt):
    return termcode(90) + txt + termcode(0)
def bold_str(txt):
    return termcode(1) + txt + termcode(0)

def print_error(s, fatal=False):
    print red_str('\n[ERROR] ' + s + '\n')
    if fatal:
        sys.exit(1)

def print_warning(s):
    print yellow_str('\n[WARNING] ' + s + '\n')

#################################################################
# HTML
#################################################################
table_style = """
<style>
    table.simple_table a:link {
        color: #666;
        font-weight: bold;
        text-decoration:none;
    }

    table.simple_table {
        font-family:Arial, Helvetica, sans-serif;
        color:#666;
        font-size:14px;
        text-shadow: 1px 1px 0px #fff;
        background:#eaebec;
        margin:auto;
        border:#ccc 1px solid;

        -moz-border-radius:3px;
        -webkit-border-radius:3px;
        border-radius:3px;

        -moz-box-shadow: 0 1px 2px #d1d1d1;
        -webkit-box-shadow: 0 1px 2px #d1d1d1;
        box-shadow: 0 1px 2px #d1d1d1;
    }
    table.simple_table th {
        padding:21px 25px 22px 25px;
        border-top:1px solid #fafafa;
        border-bottom:1px solid #e0e0e0;

        background: #ededed;
        background: -webkit-gradient(linear, left top, left bottom, from(#ededed), to(#ebebeb));
        background: -moz-linear-gradient(top,  #ededed,  #ebebeb);
    }
    table.simple_table tr {
        text-align: center;
        padding-left:20px;
    }
    table.simple_table td {
        padding:18px;
        border-top: 1px solid #ffffff;
        border-bottom:1px solid #e0e0e0;
        border-left: 1px solid #e0e0e0;

        background: #fafafa;
        background: -webkit-gradient(linear, left top, left bottom, from(#fbfbfb), to(#fafafa));
        background: -moz-linear-gradient(top,  #fbfbfb,  #fafafa);
    }
</style>
"""

def html_table(table):
    resp = ''
    resp += table_style
    resp += '<table class="simple_table">\n'
    for row in table:
        resp += "  <tr>\n"
        for col in row:
            resp += "    <td>{}</td>\n".format(col)
        resp += "  </tr>\n"
    resp += "</table>\n"
    return resp

def html_link(txt, link):
    return '<a href="{}">{}</a>'.format(link, txt)

#################################################################
# OS, Terminal, and Environment
#################################################################

def cmd(c, wait=True, noisy=False):
    # this seems to be much faster for the simple case
    if wait and not noisy:
        return commands.getoutput(c)

    if not wait:
        process = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        return

    if noisy:
        process = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output = ''
        while True:
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() != None:
                break
            output += nextline
            sys.stdout.write(nextline)
            sys.stdout.flush()
        return output.rstrip()
    else:
        process = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output = process.communicate()[0]
        return output.rstrip()

def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])

#################################################################
# math
#################################################################

def average(l):
    if not l or len(l) == 0:
        return 0.0
    return (sum(l)/len(l))

def stddev(l):
    avg = average(l)
    var = map(lambda x: (x-avg)**2, l)
    res = math.sqrt(average(var))

def median(lst):
    import numpy
    return numpy.median(numpy.array(lst)) if lst else 0

def p95(lst):
    import numpy
    return numpy.percentile(numpy.array(lst), 95) if lst else 0

def percentile(lst, n):
    """Return the n-th percentile of the list"""
    import numpy
    return numpy.percentile(numpy.array(lst), n) if lst else 0
    return res
    return res

def distance_between(lat1, long1, lat2, long2):
    """Return the distance between 2 lat/lng pairs in km"""

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))

    try:
        arc = math.acos( cos )
    except:
        # a bad acos means we are at 0 dist i think
        return 0.0

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    # 6371 is the radius in KM
    return (arc * 6371)

#################################################################
# Multiprocessing stuff
#################################################################

def get_config_int(cname, default=0):
    try:
        f = open(cname).read().strip()
        r = int(f)
        return r
    except:
        return default

def create_fbglobal(name, val=0):
    f = open('/tmp/' + name, 'w')
    f.write(str(val))
    f.close()
    for x in range(val):
        increment_fbglobal(name)

def get_fbglobal(name):
    f = open('/tmp/' + name, 'r')
    res = f.read()
    f.close()
    return len(res)

def increment_fbglobal(name, amt=1):
    f = open('/tmp/' + name, 'a')
    f.write('x')
    f.close()
    return get_fbglobal(name)
