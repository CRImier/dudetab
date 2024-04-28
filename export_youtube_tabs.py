import operator
import random
import re
import json

import common

import yt_dlp

out_file = "INSERT FILENAME HERE"

cl = common.get_client()
tabs = common.parse_tabs(cl)

def ask_tab_action(tab):
    message = "Save tab?"
    prompt = "[s]ave? [l]eave? [c]lose? [q]uit? >>> "
    print(message)
    result = None
    valid_options = "slcq"
    valid_options += valid_options.upper()
    while not result or (result not in valid_options or len(result) > 1):
        result = input(prompt)
    if result.lower() == 's':
        return "save"
    elif result.lower() == 'l':
        return "leave"
    elif result.lower() == 'c':
        return "close"
    elif result.lower() == 'q':
        return "quit"
    else:
        FunniException = type("FunniException", (Exception,), {})
        raise FunniException

# closing YouTube Home tabs

youtube_home_tabs = [tab for tab in tabs if tab.url.endswith("youtube.com/")]

for tab in youtube_home_tabs:
    print("Closing YouTube home tab in window {}".format(tab.window))
    cl.close_tabs([tab.get_full_id()])

youtube_tabs = [tab for tab in tabs if "youtube.com/watch" in tab.url]

tabs_to_close = []

# first loop: downloading

for i, tab in enumerate(youtube_tabs):
    ydl_opts = {}
    print("Downloading tab info {}/{}".format(i+1, len(youtube_tabs)))
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(tab.url, download=False, process=False)
        sinfo = ydl.sanitize_info(info)
        tab.sinfo = sinfo

# DURATION

for i, tab in enumerate(youtube_tabs):
    name = tab.name
    pattern = re.compile("^\(\d*\)\s(.*)$")
    match = pattern.match(name)
    if match:
        #print("pattern (NUMBER) matched!")
        name = match.groups()[0]
    end = ' - YouTube'
    if name.endswith(end):
        name = name[:-len(end)]
    n = "{}/{}".format(i+1, len(youtube_tabs))
    s = "{} - '{}', from {}".format(tab.url, name, tab.sinfo.get("uploader", "[UNKNOWN]"))
    print(n, s)
    result = ask_tab_action(tab)
    if result == "close":
        tabs_to_close.append(tab)
    elif result == "leave":
        continue
    elif result == "save":
        with open(out_file, 'a') as f:
            f.write(s+'\n')
        tabs_to_close.append(tab)
    elif result == "quit":
        break

for tab in tabs_to_close:
    print("Closing tab {}".format(tab.get_full_id()))
    cl.close_tabs([tab.get_full_id()])
