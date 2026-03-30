import traceback
import operator
import random
import json
import re

import common

import yt_dlp

out_file = "INSERT FILENAME HERE"

cl = common.get_client()
tabs = common.parse_tabs(cl)

FunniException = type("FunniException", (Exception,), {})

def get_url(url):
    list_marker = "&list="
    if "&list=" in url:
        url = url.split(list_marker, 1)[0]
    if "/shorts/" in url:
        url = url.replace("/shorts/", "watch?v=")
    if "/live/" in url:
        url = url.replace("/live/", "watch?v=")
    return url

# closing YouTube Home tabs

youtube_home_tabs = [tab for tab in tabs if tab.url.endswith("youtube.com/")]

for tab in youtube_home_tabs:
    print("Closing YouTube home tab in window {}".format(tab.window))
    cl.close_tabs([tab.get_full_id()])

youtube_tabs = [tab for tab in tabs if "youtube.com/watch" in get_url(tab.url)]

tabs_to_close = []

# first loop: downloading

for i, tab in enumerate(youtube_tabs):
    ydl_opts = {}
    print("Downloading tab info {}/{}".format(i+1, len(youtube_tabs)))
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            url = get_url(tab.url)
            info = ydl.extract_info(url, download=False, process=False)
            sinfo = ydl.sanitize_info(info)
            tab.sinfo = sinfo
            duration = tab.sinfo.get("duration", 0)
            if duration is None: duration = 0
            duration_m = duration // 60
            duration_s = duration % 60
            print(duration_m, duration_s)
    except yt_dlp.utils.DownloadError as e:
        traceback.print_exc()
        tab.sinfo = {}
    except Exception as e:
        traceback.print_exc()
        tab.sinfo = {}

# DURATION

for i, tab in enumerate(youtube_tabs):
    try:
        name = tab.name
        pattern = re.compile("^\(\d*\)\s(.*)$")
        match = pattern.match(name)
        if match:
            #print("pattern (NUMBER) matched!")
            name = match.groups()[0]
        end = ' - YouTube'
        if name.endswith(end):
            name = name[:-len(end)]
        duration = tab.sinfo.get("duration", 0)
        if duration is None: duration = 0
        duration_m = duration // 60
        duration_s = duration % 60
        n = "{}/{}".format(i+1, len(youtube_tabs))
        url = get_url(tab.url)
        s = "{} - '{}' ({}:{}), from {}".format(tab.url, name, duration_m, duration_s, tab.sinfo.get("uploader", "[UNKNOWN]"))
        print(n, s)
        result = ask_tab_action("Save tab?", answers = ["[s]ave", "[l]eave", "[c]lose", "[q]uit"])
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
    except:
        traceback.print_exc()

cl = common.get_client()
tabs = common.parse_tabs(cl)
tab_ids = [tab.get_full_id() for tab in tabs]

try:
    for tab in tabs_to_close:
        tab_id = tab.get_full_id()
        if tab_id in tab_ids: # don't you dare trying and close the tab that's already been closed - that's either data loss, or a crash
            print("Closing tab {}".format(tab_id))
            cl.close_tabs([tab_id])
except:
    traceback.print_exc()
    print(tabs_to_close)
