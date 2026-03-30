import operator

from common import *

cl = get_client()
tabs = parse_tabs(cl)

bsky_marker = "https://bsky.app"

bsky_tabs = [tab for tab in tabs if bsky_marker in tab.url]

# all tabs containing bluesky windows right now

bluesky_windows = {}
for tab in bsky_tabs:
    if tab.window not in bluesky_windows:
        bluesky_windows[tab.window] = 1
    else:
        bluesky_windows[tab.window] += 1

min_window = str(min([map(int, bluesky_windows.keys())]))

# first tab is me-specific thing

first_tab_ignored = False
first_tab = None

# tagging the first tab that's pinned in my first browser window
for tab in bsky_tabs:
    if tab.window == min_window:
        if not first_tab_ignored:
            first_tab = tab
            #first_tab_ignored = True
            continue

# closing Bluesky Home tabs

for tab in bsky_tabs:
    if tab.url == bsky_marker+"/home" \
      and tab != first_tab:
        print("Closing home tab:", tab.get_full_id())
        cl.close_tabs([tab.get_full_id()])

for tab in bsky_tabs:
    if tab.url == "https://bsky.app/notifications" \
      and tab != first_tab:
        print("Closing notif tab:", tab.get_full_id())
        cl.close_tabs([tab.get_full_id()])

for tab in bsky_tabs:
    if tab.url == "https://bsky.app/" \
      and tab != first_tab:
        print("Closing feed tab:", tab.get_full_id())
        cl.close_tabs([tab.get_full_id()])

# closed a bunch of tabs - regenerating the data

tabs = parse_tabs(cl)

bsky_tabs = [tab for tab in tabs if "https://bsky.app" in tab.url]

bluesky_windows = {}
for tab in bsky_tabs:
    if tab.window not in bluesky_windows:
        bluesky_windows[tab.window] = 1
    else:
        bluesky_windows[tab.window] += 1

# determining a window where the majority of Bluesky tabs are

largest_window = max(bluesky_windows.items(), key=operator.itemgetter(1))[0]

# moving all the tabs into that window
# the process is involved since you need to recalculate tab indices - I'd rather rely on the brotab code for that

old_tabs = serialize_tabs(tabs)

#print(bsky_tabs)

for tab in bsky_tabs:
    if tab.window == min_window:
        if not first_tab_ignored:
            first_tab_ignored = True
            continue
    if tab.window != largest_window:
        print("Moving tab {} from window {} to window {}".format(tab.get_full_id(), tab.window, largest_window))
        tab.window = largest_window

new_tabs = serialize_tabs(tabs)
# this code recalculates the tab indices and also calls the move command
update_tabs(cl, old_tabs, new_tabs)

tabs = parse_tabs(cl)

# cleaning the bluesky window from anything that's not bluesky

# TODO - can't open a new window to dump tabs into, so, need to think of other way to clean up the bluesky window

"""
bluesky_window_tabs = [tab for tab in tabs if tab.window == bluesky_window]
unrelated_tabs = [tab for tab in bluesky_window_tabs if "//bsky.app" not in tab.url]

for tab in unrelated_tabs:
    if tab.url == "https://bsky.app/home":
        break
        #print("Closing home tab:", tab.get_full_id())
        #cl.close_tabs([tab.get_full_id()])
"""

import close_empty_windows
