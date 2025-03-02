import requests
import time
import json
from collections import defaultdict

def bg_color_txt(text, bg_color, text_color):
    colors = {
        # Background colors
        "yellow_bg": "\033[43m",
        "blue_bg": "\033[44m", 
        "red_bg": "\033[41m",
        "green_bg": "\033[42m",
        "orange_bg": "\033[48;5;208m",
        "purple_bg": "\033[45m",
        "light_green_bg": "\033[48;5;120m",
        "brown_bg": "\033[48;5;130m",
        "light_blue_bg": "\033[48;5;39m",
        "dark_green_bg": "\033[48;5;22m",
        "gray_bg": "\033[48;5;240m",
        "dark_gray_bg": "\033[48;5;235m",
        
        # Text colors
        "black_text": "\033[30m",
        "white_text": "\033[37m",
        
        # Reset
        "reset": "\033[0m"
    }
    
    return f"{colors[bg_color]}{colors[text_color]}{text}{colors['reset']}"

# NYC Subway lines with their official colors
nyc_subway = {k: f"({v})" for k,v in {
    # IRT Lines (1, 2, 3, 4, 5, 6, 7)
    "1": bg_color_txt("1", "red_bg", "white_text"),
    "2": bg_color_txt("2", "red_bg", "white_text"),
    "3": bg_color_txt("3", "red_bg", "white_text"),
    "4": bg_color_txt("4", "green_bg", "white_text"),
    "5": bg_color_txt("5", "green_bg", "white_text"),
    "6": bg_color_txt("6", "green_bg", "white_text"),
    "7": bg_color_txt("7", "purple_bg", "white_text"),
    
    # IND Lines (A, B, C, D, E, F, G)
    "A": bg_color_txt("A", "blue_bg", "white_text"),
    "C": bg_color_txt("C", "blue_bg", "white_text"),
    "E": bg_color_txt("E", "blue_bg", "white_text"),
    "B": bg_color_txt("B", "orange_bg", "black_text"),
    "D": bg_color_txt("D", "orange_bg", "black_text"),
    "F": bg_color_txt("F", "orange_bg", "black_text"),
    "M": bg_color_txt("M", "orange_bg", "black_text"),
    "G": bg_color_txt("G", "light_green_bg", "white_text"),
    
    # BMT Lines (J, Z, L, N, Q, R, W)
    "J": bg_color_txt("J", "brown_bg", "white_text"),
    "Z": bg_color_txt("Z", "brown_bg", "white_text"),
    "L": bg_color_txt("L", "gray_bg", "white_text"),
    "N": bg_color_txt("N", "yellow_bg", "black_text"),
    "Q": bg_color_txt("Q", "yellow_bg", "black_text"),
    "R": bg_color_txt("R", "yellow_bg", "black_text"),
    "W": bg_color_txt("W", "yellow_bg", "black_text"),
    
    # Shuttle
    "S": bg_color_txt("S", "dark_gray_bg", "white_text"),
}.items()}


# Get status with https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts.json

def currently_in(period):
    now = time.time()
    if start := period.get("start"):
        if start > now:
            return False
    if end := period.get("end"):
        if end < now:
            return False
    return True


def get_text(translations, n=10):
    en_txt = next(t['text'] for t in translations if t['language'] == 'en')
    return en_txt.split("\n")[0:n]

def status():
    per_line_issues = defaultdict(list)

    resp = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts.json")
    js = json.loads(resp.text)
    #print(js)
    entity = js['entity']
    for row in entity:
        #print(row)
        lines = [ie['route_id'] for ie in row['alert']['informed_entity'] if 'route_id' in ie]
        periods = row['alert']['active_period']
        if not any(currently_in(period) for period in periods):
            continue

        alert = row['alert']
        txt = []
        if "description_text" in alert:
            txt.extend(get_text(alert['description_text']['translation'], n=1))

        txt.extend(get_text(alert['header_text']['translation'], n=10))

        #print(f"{lines} : {txt}")
        for line in lines:
            per_line_issues[line].extend(txt)

    return per_line_issues

s = status()
for line, colored_symbol in nyc_subway.items():
    line_status = "\n      ".join(s.get(line, []))
    print(f"{colored_symbol} : {line_status}")

