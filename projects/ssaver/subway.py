import requests
import time
import json
from collections import defaultdict


def bg_color_txt(text, bg_color, text_color, as_html=False):
    if as_html:
        html_colors = {
            # Background colors
            "yellow_bg": "#FFCC00",
            "blue_bg": "#0039A6",
            "red_bg": "#EE352E",
            "green_bg": "#00933C",
            "orange_bg": "#FF6319",
            "purple_bg": "#B933AD",
            "light_green_bg": "#6CBE45",
            "brown_bg": "#996633",
            "light_blue_bg": "#00AEEF",
            "dark_green_bg": "#00542A",
            "gray_bg": "#808183",
            "dark_gray_bg": "#404040",
            # Text colors
            "black_text": "#000000",
            "white_text": "#FFFFFF",
        }

        bg = html_colors[bg_color]
        fg = html_colors[text_color]
        return f'<span style="background-color:{bg};color:{fg};padding:0 3px;border-radius:3px;font-weight:bold;">{text}</span>'
    else:
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
            "reset": "\033[0m",
        }

        return f"{colors[bg_color]}{colors[text_color]}{text}{colors['reset']}"


# Function to generate subway line mapping with either terminal or HTML formatting
def get_nyc_subway(as_html=False):
    return {
        k: f"({v})"
        for k, v in {
            # IRT Lines (1, 2, 3, 4, 5, 6, 7)
            "1": bg_color_txt("1", "red_bg", "white_text", as_html),
            "2": bg_color_txt("2", "red_bg", "white_text", as_html),
            "3": bg_color_txt("3", "red_bg", "white_text", as_html),
            "4": bg_color_txt("4", "green_bg", "white_text", as_html),
            "5": bg_color_txt("5", "green_bg", "white_text", as_html),
            "6": bg_color_txt("6", "green_bg", "white_text", as_html),
            "7": bg_color_txt("7", "purple_bg", "white_text", as_html),
            # IND Lines (A, B, C, D, E, F, G)
            "A": bg_color_txt("A", "blue_bg", "white_text", as_html),
            "C": bg_color_txt("C", "blue_bg", "white_text", as_html),
            "E": bg_color_txt("E", "blue_bg", "white_text", as_html),
            "B": bg_color_txt("B", "orange_bg", "black_text", as_html),
            "D": bg_color_txt("D", "orange_bg", "black_text", as_html),
            "F": bg_color_txt("F", "orange_bg", "black_text", as_html),
            "M": bg_color_txt("M", "orange_bg", "black_text", as_html),
            "G": bg_color_txt("G", "light_green_bg", "white_text", as_html),
            # BMT Lines (J, Z, L, N, Q, R, W)
            "J": bg_color_txt("J", "brown_bg", "white_text", as_html),
            "Z": bg_color_txt("Z", "brown_bg", "white_text", as_html),
            "L": bg_color_txt("L", "gray_bg", "white_text", as_html),
            "N": bg_color_txt("N", "yellow_bg", "black_text", as_html),
            "Q": bg_color_txt("Q", "yellow_bg", "black_text", as_html),
            "R": bg_color_txt("R", "yellow_bg", "black_text", as_html),
            "W": bg_color_txt("W", "yellow_bg", "black_text", as_html),
            # Shuttle
            "S": bg_color_txt("S", "dark_gray_bg", "white_text", as_html),
        }.items()
    }


# Default to terminal colors
# nyc_subway = get_nyc_subway(as_html=False)


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
    en_txt = next(t["text"] for t in translations if t["language"] == "en")
    return en_txt.split("\n")[0:n]


def status():
    per_line_issues = defaultdict(list)

    resp = requests.get(
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts.json"
    )
    js = json.loads(resp.text)
    # print(js)
    entity = js["entity"]
    for row in entity:
        # print(row)
        lines = [
            ie["route_id"] for ie in row["alert"]["informed_entity"] if "route_id" in ie
        ]
        periods = row["alert"]["active_period"]
        if not any(currently_in(period) for period in periods):
            continue

        alert = row["alert"]
        txt = []
        if "description_text" in alert:
            txt.extend(get_text(alert["description_text"]["translation"], n=1))

        txt.extend(get_text(alert["header_text"]["translation"], n=10))

        # print(f"{lines} : {txt}")
        for line in lines:
            per_line_issues[line].extend(txt)

    return per_line_issues


def get_subway_status_formatted(as_html=False, linelimit=3):
    subway_map = get_nyc_subway(as_html=as_html)
    s = status()
    result = []

    for line, colored_symbol in subway_map.items():
        line_status = s.get(line, [])[0:linelimit]
        line_status = "\n      ".join(line_status)
        if as_html:
            result.append(f"{colored_symbol} : {line_status}")
        else:
            result.append(f"{colored_symbol} : {line_status}")

    if as_html:
        return "\n".join(result)
    else:
        return "\n".join(result)


if __name__ == "__main__":
    print(get_subway_status_formatted(as_html=False))
