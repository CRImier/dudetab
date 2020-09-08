import common

cl = common.get_client()
tabs = common.parse_tabs(cl)
windows = common.get_window_ids(tabs)

active_tabs = cl.get_active_tabs(None)

with open("heavy_tab_hosts.txt", "r") as f:
    lines = f.readlines()
    heavy_hosts = [line.strip() for line in lines if line.strip()]

print(heavy_hosts)

def is_empty_tab(tab):
    return tab.url == "about:newtab" or tab.url == "about:home"

def is_heavy_tab(tab):
    return any([host in tab.url for host in heavy_hosts])

for tab in tabs:
    if tab.get_full_id() in active_tabs:
        print("{}: {} ({})".format(tab.window, tab.name, tab.url))
        if not common.is_empty_tab(tab) and is_heavy_tab(tab):
            # tab that's currently open is not empty and is a heavy one to hold in-memory
            # so, we need to either switch to an empty tab in the same window or open a new empty tab in the same window
            window = tab.window
            tabs_by_window = common.filter_tabs_by_window(tabs, window)
            # going through the window's tabs in reverse - so we switch to last open empty tab
            for tabw in list(reversed(tabs_by_window)):
                if is_empty_tab(tabw):
                    #print('Switching from "{}" to "{}" in window {}'.format(tab.name, tabw.name, window))
                    cl.activate_tab([tabw.get_full_id()], False)
                    break
            else: # no empty tab in the window found
                print("Opening a blank tab in \"{}\" window ({})".format(tab.name, window))
                cl.open_urls(["about:blank"], window_id=window)
