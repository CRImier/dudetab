import operator

from brotab import api as brapi

import common

cl = common.get_client()
tabs = common.parse_tabs(cl)
windows = common.get_window_ids(tabs)

def is_empty_tab(tab):
    return tab.url == "about:newtab" or tab.url == "about:home"

# going through tabs and, for each tab that's not empty, filtering out the window that contains it
# after that, the windows left over will only contain empty tabs
for tab in tabs:
    if not is_empty_tab(tab) and tab.window in windows:
        windows.remove(tab.window)

# closing each tab one-by-one
for tab in tabs:
    if is_empty_tab(tab) and tab.window in windows:
        print("Closing empty tab {}".format(tab.get_full_id()))
        cl.close_tabs([tab.get_full_id()])
