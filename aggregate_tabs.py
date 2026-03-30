import operator
import random

import common

import aggregate_youtube_tabs_simpl
import aggregate_bsky_tabs
import save_bsky_images
import save_discord_images

cl = common.get_client()
tabs = common.parse_tabs(cl)

newtab = "about:newtab"

print("starting general aggregation")

def get_windows():
    windows = {}
    for tab in tabs:
        if tab.window not in windows:
            windows[tab.window] = [tab]
        else:
            windows[tab.window].append(tab)
    return windows

windows = get_windows()

main_win = None
yt_win = None
bs_win = None

for winnum, tabs in windows.items():
    has_yandex = any(["yandex.com" in tab.url for tab in tabs]) # my personal heuristic for my main tab
    has_performance = any(["about:processes" in tab.url for tab in tabs]) or any(["about:performance" in tab.url for tab in tabs])
    has_youtube = any([aggregate_youtube_tabs_simpl.yt_marker in tab.url for tab in tabs])
    has_bsky = any([aggregate_bsky_tabs.bsky_marker in tab.url for tab in tabs])
    if has_yandex and has_performance:
        print("Main window found", winnum)
        if main_win != None:
            # ALERT break down break down
            print("Duplicate main window found?", winnum)
            import sys; sys.exit(1)
        main_win = winnum
    if has_youtube:
        # assuming youtube windows are already aggregated
        print("YouTube window found", winnum)
        if yt_win != None:
            # ALERT break down break down
            print("Duplicate YouTube window found?", winnum)
            import sys; sys.exit(2)
        yt_win = winnum
    if has_bsky:
        # assuming youtube windows are already aggregated
        print("Bluesky window found", winnum)
        if bs_win != None:
            # ALERT break down break down
            print("Duplicate Bluesky window found?", winnum)
            import sys; sys.exit(3)
        bs_win = winnum

used_windows = [main_win, yt_win, bs_win]

tab_counts = []

for winnum, tabs in windows.items():
    if winnum not in used_windows:
        tab_counts.append([winnum, len(tabs)])

tabs = common.parse_tabs(cl)

tab_counts_sorted = list(reversed(sorted(tab_counts, key=lambda x: x[1])))
ca_win = tab_counts_sorted[0][0] # catchall window for whatever-else-is-going-on
print("Catchall window decided: {} ({} tabs)".format(ca_win, len(windows[ca_win])))

# now starting to move stuff into catchall window
old_tabs = common.serialize_tabs(tabs)
bsky_tabs = common.filter_tabs_by_window(tabs, bs_win)
#print(len(tabs), common.get_window_ids(tabs))
for tab in bsky_tabs:
    # bsky window tab is impostor
    if aggregate_bsky_tabs.bsky_marker not in tab.url and newtab not in tab.url:
        print("Moving non-Bsky tab {} {} from Bsky window {} to CA window {}".format(tab.get_full_id(), tab.url, tab.window, ca_win))
        tab.window = ca_win
new_tabs = common.serialize_tabs(tabs)
# this code recalculates the tab indices and also calls the move command
common.update_tabs(cl, old_tabs, new_tabs)
tabs = common.parse_tabs(cl)

old_tabs = common.serialize_tabs(tabs)
yt_tabs = common.filter_tabs_by_window(tabs, yt_win)
#print(len(tabs), common.get_window_ids(tabs))
for tab in yt_tabs:
    # bsky window tab is impostor
    if "youtube.com/" not in tab.url and newtab not in tab.url:
        print("Moving non-YT tab {} {} from YT window {} to CA window {}".format(tab.get_full_id(), tab.url, tab.window, ca_win))
        tab.window = ca_win
new_tabs = common.serialize_tabs(tabs)
# this code recalculates the tab indices and also calls the move command
common.update_tabs(cl, old_tabs, new_tabs)
tabs = common.parse_tabs(cl)


# yeeting all unrelated tabs from main window
cutoff = [i for i, tab in enumerate(common.filter_tabs_by_window(tabs, main_win)) if tab.url == newtab][0]
other_tabs = common.filter_tabs_by_window(tabs, main_win)[(cutoff+1):]
#print(len(other_tabs))

old_tabs = common.serialize_tabs(tabs)
for tab in other_tabs:
    print("Moving non-main tab {} {} from main window {} to CA window {}".format(tab.get_full_id(), tab.url, tab.window, ca_win))
    tab.window = ca_win
new_tabs = common.serialize_tabs(tabs)
# this code recalculates the tab indices and also calls the move command
common.update_tabs(cl, old_tabs, new_tabs)
tabs = common.parse_tabs(cl)

used_windows = [main_win, yt_win, bs_win, ca_win]

# yeeting all small window tabs into the catchall window
windows = get_windows()
for window in windows:
    if window not in used_windows:
        old_tabs = common.serialize_tabs(tabs)
        moveable_tabs = common.filter_tabs_by_window(tabs, window)
        for tab in moveable_tabs:
            print("Moving non-main tab {} {} from small window {} to CA window {}".format(tab.get_full_id(), tab.url, tab.window, ca_win))
            tab.window = ca_win
        new_tabs = common.serialize_tabs(tabs)
        # this code recalculates the tab indices and also calls the move command
        common.update_tabs(cl, old_tabs, new_tabs)
        tabs = common.parse_tabs(cl)

# now, closing empty windows
windows = [yt_win, bs_win, ca_win]
for win_num in windows:
    newtabs = [tab for tab in common.filter_tabs_by_window(tabs, win_num) if tab.url == newtab]
    #print(win_num, len(newtabs))
    if len(newtabs) > 1:
        for i, tab in enumerate(newtabs):
            if i == len(newtabs)-1: continue # last newtab may stay untouched
            cl.close_tabs([tab.get_full_id()])
        print("Closed {} empty tabs in window {}".format(len(newtabs)-1, win_num))
