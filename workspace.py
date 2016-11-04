#!/usr/bin/env python3
#
# script that controls i3 workspaces

# different states:
# focused (white)
# urgent (red)
# visible (grey)
# not supported with pngs

import getopt
import signal
import subprocess
import json
import sys
import time
import os

from ws_config import WS_CONFIG 
from ws_config import IMG_FOLDER 

INTERVAL = 200
FA_EMPTY = "<span font='FontAwesome'>\uf055</span>"
FA_FIREFOX = "<span font='FontAwesome'>\uf269</span>"
FA_TERMINAL = "<span font='FontAwesome'>\uf120</span>"
COLOR_FOCUSED = "white"
COLOR_UNFOCUSED = "#787f83"

IMG_NULL_PATH = 'null.png'

I3_MSG_COMMAND_TREE = ['i3-msg', '-t', 'get_tree']
I3_MSG_COMMAND_WORKSPACES = ['i3-msg', '-t', 'get_workspaces']

def get_symbol(application):
    mapping = {
        'Firefox': FA_FIREFOX,
        'konsole': FA_TERMINAL
    }
    return mapping.get(application, "")

def get_symbols(applications):
    symbols = ""
    for application in applications:
        symbols += " " + get_symbol(application)
    return symbols

def get_windows(myjson):
    if type(myjson) is dict:
        if myjson['type'] == 'con' and myjson['window'] is None:
            #container
            windows = []
            for element in myjson['nodes']:
                windows += get_windows(element)
            return windows
        else:
            #window
            return [myjson['window_properties']['class']]
    elif type(myjson) is list:
        windows = []
        for element in myjson:
            windows += get_windows(element)
        return windows

def get_workspaces(myjson):
    result = []
    if type(myjson) is dict:
        if myjson['type'] == 'workspace' and myjson['name'] != '__i3_scratch':
            ws = {}
            ws['windows'] = get_windows(myjson['nodes'])
            ws['name'] = myjson['name']
            ws['num'] = myjson['num']
            result.append(ws)
        else:
            result += get_workspaces(myjson['nodes'])
    elif type(myjson) is list:
        for element in myjson:
             result += get_workspaces(element)
    return result

def merge_windows_with_config(ws_json, ws_win_json):
    wss = []
    for ws in ws_json:
        for ws_win in ws_win_json:
            if ws['num'] == ws_win['num']:
                # and name
                #ws['name'] = shortws['name']
                #ws['visible'] = shortws['visible']
                ws_new = {}
                ws_new['num'] = ws['num']
                ws_new['urgent'] = ws['urgent']
                ws_new['focused'] = ws['focused']
                ws_new['windows'] = ws_win['windows']
                wss.append(ws_new)
    return wss

def find_config(arg_num):
    found = False
    for ws_config in WS_CONFIG:
        if ws_config['num'] == int(arg_num):
            global num
            num = int(arg_num)
            global config
            config = ws_config
            global display_type
            if 'name' in config:
                global name
                name = config['name']
                display_type = 'char'
            else:
                global img_path
                img_path = config['img']
                display_type = 'img'
            global key
            key = config['key']
            found = True
            break
    if not found:
        print("no ws with num", arg_num, "found")
        sys.exit(2)


def update():
    workspace_string = subprocess.check_output(I3_MSG_COMMAND_WORKSPACES, universal_newlines=True)
    ws_json = json.loads(workspace_string)
    visible = False
    color = COLOR_UNFOCUSED
    urgent = False
    for ws in ws_json:
        if ws['num'] == num:
            visible = True
            if ws['focused']:
                color = COLOR_FOCUSED
            if ws['urgent']:
                urgent = True
    if not visible:
        print("")
        sys.stdout.flush()
    else:
        # clear bg img
        file_path = '{}/ws{}_current.png'.format(IMG_FOLDER, num)
        if os.path.islink(file_path):
            os.remove(file_path)
        src = IMG_NULL_PATH

        if display_type is 'char':
            #if config['static']:
            fulltext = "<span rise='13000' size='7000' foreground='{}'> {}<span rise='0' size='15000'> {} </span></span> ".format(color, key, name)
        else:
            if ws['focused']:
                src = img_path[0]
            else:
                src = img_path[1]
            fulltext = "         "

        os.symlink(src, file_path)
        print(fulltext)
        time.sleep(0.05)
        sys.stdout.flush()

        #tree_string = check_output(I3_MSG_COMMAND_TREE, universal_newlines=True)

def handle_signal(signum, stack):
    if signum == signal.SIGUSR2:
        update()


def persistant(arg):
    signal.signal(signal.SIGUSR1, handle_signal)
    signal.signal(signal.SIGUSR2, handle_signal)
    find_config(arg)
    while True:
        update()
        time.sleep(INTERVAL)

def main(argv):
    try:
        opts, args = getopt.getopt(argv,'vk:')
    except getopt.GetoptError:
        print('workspace.py [-k key|-v]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-v':
            print('workspace.py v0.1')
            sys.exit()
        elif opt == '-k':
            persistant(arg)
    print('workspace.py [-k|-v]')
    sys.exit(2)

last_fulltext = ''
main(sys.argv[1:])

