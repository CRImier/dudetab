import operator

import common

cl = common.get_client()
tabs = common.parse_tabs(cl)

bsky_tabs = [tab for tab in tabs if "https://bsky.app" in tab.url]

# closing Bluesky Home tabs

for tab in bsky_tabs:
    if tab.url == "https://bsky.app/home":
        print("Closing home tab:", tab.get_full_id())
        cl.close_tabs([tab.get_full_id()])

# determining a window where the majority of Bluesky tabs are

bluesky_windows = {}
for tab in bsky_tabs:
    if tab.window not in bluesky_windows:
        bluesky_windows[tab.window] = 1
    else:
        bluesky_windows[tab.window] += 1

largest_window = max(bluesky_windows.items(), key=operator.itemgetter(1))[0]

# moving all the tabs into that window
# the process is involved since you need to recalculate tab indices - I'd rather rely on the brotab code for that

old_tabs = common.serialize_tabs(tabs)

#print(bsky_tabs)

# first tab is me-specific thing

first_tab_ignored = False

for tab in bsky_tabs:
    if tab.window == '1':
        if not first_tab_ignored:
            first_tab_ignored = True
            continue
    if tab.window != largest_window:
        print("Moving tab {} from window {} to window {}".format(tab.get_full_id(), tab.window, largest_window))
        tab.window = largest_window

new_tabs = common.serialize_tabs(tabs)
# this code recalculates the tab indices and also calls the move command
common.update_tabs(cl, old_tabs, new_tabs)

tabs = common.parse_tabs(cl)

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

