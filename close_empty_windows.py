from common import *

cl = get_client()
tabs = parse_tabs(cl)
windows = get_window_ids(tabs)

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
