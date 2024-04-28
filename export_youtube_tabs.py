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

breakpoint()


import sys;sys.exit(0)







youtube_windows = {}
for tab in youtube_tabs:
    if tab.window not in youtube_windows:
        youtube_windows[tab.window] = 1
    else:
        youtube_windows[tab.window] += 1

print(youtube_windows)

large_windows = {}

tabs_to_close = []
non_music_tabs = []

for window, count in youtube_windows.items():
    large_windows[window] = count
    print("Large window {} has {} tabs".format(repr(window), count))

largest_window = max(large_windows.items(), key=operator.itemgetter(1))[0]

# regenerate all the variables we'll be using
tabs = common.parse_tabs(cl)
youtube_tabs = [tab for tab in tabs if "youtube.com" in tab.url]

print(large_windows, largest_window)

for window in large_windows:
    print("Processing {}".format(window))
    if window == largest_window:
        continue
    print("Processing {}".format(window))
    old_tabs = common.serialize_tabs(tabs)
    window_tabs = common.filter_tabs_by_window(tabs, window)
    youtube_tabs = [tab for tab in window_tabs if "youtube.com" in tab.url]
    for tab in youtube_tabs:
        print("Moving tab {} from window {} to window {}".format(tab.get_full_id(), tab.window, largest_window))
        tab.window = largest_window
    new_tabs = common.serialize_tabs(tabs)
    # this code recalculates the tab indices and also calls the move command
    common.update_tabs(cl, old_tabs, new_tabs)
    tabs = common.parse_tabs(cl)

other_windows = [window for window in youtube_windows.keys() if window not in large_windows]

if other_windows:
    print("Other windows: {}".format(other_windows))
else:
    print("Sorting finished, no small windows found!")
    import sys;sys.exit(0)
