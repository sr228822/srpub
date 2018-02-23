#!/usr/bin/python

import sys

CODE={
    'ENDC':0,  # RESET COLOR
    'BOLD':1,
    'UNDERLINE':4,
    'GREEN':32,
    'GREY':90,
    'RED':91,
    'YELLOW':93,
    'BLUE':34, #94

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

def print_color(color,txt):
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
