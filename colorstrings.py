#!/usr/bin/python

from __future__ import print_function

import re, sys, random

CODE={
    'ENDC':0,  # RESET COLOR

    'BOLD':1,
    'UNDERLINE':4,
    'BLINK': 5,

    'GREEN':32,
    'GREY':90,
    'RED':91,
    'YELLOW':93,
    'BLUE':34,
    'LIGHT_BLUE': 94,
    'CYAN': 36,
    'MAGENTA': 95,

    'RED_BG':41,
    'GREEN_BG':42,
    'YELLOW_BG':43,
    'BLUE_BG':44,
}

def termcode(num):
    return '\033[%sm'%num

def color_str(txt,color):
    return termcode(CODE[color.upper()])+txt+termcode(CODE['ENDC'])

def dual_color_str(txt,fgcolor,bgcolor):
    return termcode(CODE[fgcolor.upper()]) + termcode(CODE[bgcolor.upper() + "_BG"]) + txt + termcode(CODE['ENDC'])

def bg_color_str(txt,color):
    return termcode(CODE[color.upper() + "_BG"]) + txt + termcode(CODE['ENDC'])

i = 0
colors = ['red', 'magenta', 'green', 'blue', 'yellow', 'cyan']
def print_color(color,txt):
    global i, colors
    if color == 'rainbow':
        words = re.findall(r'(\S+)', txt)
        for word in words:
            txt = txt.replace(word, color_str(word, colors[i]))
            i = (i + 1) % len(colors)
        print(txt)
    else:
        print(color_str(txt, color))

# unnecessary helper funcs
def grey_str(text):
    return color_str(text,'GREY')
def bold_str(text):
    return color_str(text,'BOLD')
def underline_str(text):
    return color_str(text,'UNDERLINE')
def red_str(text):
    return color_str(text,'RED')
def blue_str(text):
    return color_str(text,'BLUE')
def green_str(text):
    return color_str(text,'GREEN')
def yellow_str(text):
    return color_str(text,'YELLOW')
def rainbow_str(text):
    c = random.choice(CODE.keys())
    return color_str(text, c)

def print_grey(text):
    print(grey_str(text))
def print_bold(text):
    print(bold_str(text))
def print_underline(text):
    print(underline_str(text))
def print_red(text):
    print(red_str(text))
def print_blue(text):
    print(blue_str(text))
def print_green(text):
    print(green_str(text))
def print_yellow(text):
    print(yellow_str(text))

if __name__ == "__main__":
    # flexibly print args or piped input
    if len(sys.argv) == 1:
        print_color("rainbow", "what color did you want")
    elif len(sys.argv) == 2:
        color = sys.argv[1].lower()
        deadlines = 0
        while True:
            text = sys.stdin.readline().rstrip()
            if text:
                for i in range(deadlines):
                    print('')
                deadlines = 0
                print_color(color,text)
            else:
                deadlines += 1
                if deadlines > 5:
                    break
    else:
        color = sys.argv[1].lower()
        text = " ".join(sys.argv[2:])
        print_color(color,text)
