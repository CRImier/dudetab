import operator

from brotab import api as brapi

import common

cl = common.get_client()
tabs = common.parse_tabs(cl)

twitter_tabs = [tab for tab in tabs if "twitter.com" in tab.url]

# closing Twitter Home tabs

for tab in twitter_tabs:
    if tab.url == "https://twitter.com/home":
        print("Closing home tab:", tab.get_full_id())
        cl.close_tabs([tab.get_full_id()])

# determining a window where the majority of Twitter tabs are

twitter_windows = {}
for tab in twitter_tabs:
    if tab.window not in twitter_windows:
        twitter_windows[tab.window] = 1
    else:
        twitter_windows[tab.window] += 1

largest_window = max(twitter_windows.items(), key=operator.itemgetter(1))[0]

# moving all the tabs into that window
# the process is involved since you need to recalculate tab indices - I'd rather rely on the brotab code for that

old_tabs = common.serialize_tabs(tabs)

for tab in twitter_tabs:
    if tab.window != largest_window:
        print("Moving tab {} from window {} to window {}".format(tab.get_full_id(), tab.window, largest_window))
        tab.window = largest_window

new_tabs = common.serialize_tabs(tabs)
# this code recalculates the tab indices and also calls the move command
common.update_tabs(cl, old_tabs, new_tabs)

tabs = common.parse_tabs(cl)

# cleaning the Twitter window from anything that's not Twitter

# TODO - can't open a new window to dump tabs into, so, need to think of other way to clean up the Twitter window

"""
twitter_window_tabs = [tab for tab in tabs if tab.window == twitter_window]
unrelated_tabs = [tab for tab in twitter_window_tabs if "//twitter.com" not in tab.url]

for tab in unrelated_tabs:
    if tab.url == "https://twitter.com/home":
        break
        #print("Closing home tab:", tab.get_full_id())
        #cl.close_tabs([tab.get_full_id()])
"""

