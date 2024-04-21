import operator
import random

import common

##################################################
# Variable names are very outdated here istg like
# do not trust the variable names
# they will deceive you
##################################################

cl = common.get_client()
tabs = common.parse_tabs(cl)

# closing YouTube Home tabs

youtube_home_tabs = [tab for tab in tabs if tab.url.endswith("youtube.com/")]

for tab in youtube_home_tabs:
    print("Closing YouTube home tab in window {}".format(tab.window))
    cl.close_tabs([tab.get_full_id()])

youtube_tabs = [tab for tab in tabs if "youtube.com" in tab.url]

# determining a window where the majority of YouTube tabs are

youtube_windows = {}
for tab in youtube_tabs:
    if tab.window not in youtube_windows:
        youtube_windows[tab.window] = 1
    else:
        youtube_windows[tab.window] += 1

print(youtube_windows)

large_windows = {}

tabs_to_close = []

for window, count in youtube_windows.items():
    large_windows[window] = count
    print("Large window {} has {} tabs".format(repr(window), count))


largest_window = max(large_windows.items(), key=operator.itemgetter(1))[0]

# regenerate all the variables we'll be using
tabs = common.parse_tabs(cl)
youtube_tabs = [tab for tab in tabs if "youtube.com" in tab.url]

# merge all large non-music windows together with the largest window

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
