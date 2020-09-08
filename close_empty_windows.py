import common

cl = common.get_client()
tabs = common.parse_tabs(cl)
windows = common.get_window_ids(tabs)

# going through tabs and, for each tab that's not empty, filtering out the window that contains it
# after that, the windows left over will only contain empty tabs
for tab in tabs:
    if not common.is_empty_tab(tab) and tab.window in windows:
        windows.remove(tab.window)

# closing each tab one-by-one
for tab in tabs:
    if common.is_empty_tab(tab) and tab.window in windows:
        print("Closing empty tab {}".format(tab.get_full_id()))
        cl.close_tabs([tab.get_full_id()])
