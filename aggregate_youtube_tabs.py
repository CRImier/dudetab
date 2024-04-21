import operator
import random

# This script assumes that the user has a large window full of YouTube tabs with music, and a large window that has non-music tabs.
# The user also opens YouTube tabs in other windows from time to time - music or not music.
# The script assumes there's only one large (>30) all-music window currently open.
# This is, as you can guess, my usage scenario.

# Before everything, the script closes all the YouTube homepage tabs.
# First, the script goes through each large window and ask users whether tabs in it are music or non-music tabs
# once a window with enough music tabs is found, it's determined to be a music window
# All the other large windows are merged together into whatever non-music window is the largest.
# Then, for each small window (window that doesn't contain a lot of YouTube tabs, no matter the count of other tabs in the window),
# user has to go through every single tab and decide whether it's a music tab or not.
# This way, tabs can be sorted properly, even if there's a large window with both music tabs and non-music tabs.
# Also, after a window is decided to be a music window, the script moves all the tabs marked by user as non-music tabs out of it.

import common

cl = common.get_client()
tabs = common.parse_tabs(cl)

# closing YouTube Home tabs

youtube_home_tabs = [tab for tab in tabs if tab.url.endswith("youtube.com/")]

for tab in youtube_home_tabs:
    print("Closing YouTube home tab in window {}".format(tab.window))
    cl.close_tabs([tab.get_full_id()])

youtube_tabs = [tab for tab in tabs if "youtube.com" in tab.url]

# determining a window where the majority of Twitter tabs are

sorting_limit = 30

youtube_windows = {}
for tab in youtube_tabs:
    if tab.window not in youtube_windows:
        youtube_windows[tab.window] = 1
    else:
        youtube_windows[tab.window] += 1

print(youtube_windows)

music_tabs_to_check = 5
music_tab_threshold = 3

music_window = None
large_windows = {}

def ask_if_music_tab(tab, leave_option=False):
    message = 'Is this music: \"{}\"?'.format(tab.name)
    if leave_option:
        prompt = "[y]es? [N]o [l]eave? [c]lose? >>> "
    else:
        prompt = "[y]es? [N]o? [c]lose? >>> "
    print(message)
    result = None
    valid_options = "YyNnLlCc" if leave_option else "YyNnCc"
    while not result or (result not in valid_options or len(result) > 1):
        result = input(prompt)
    if result.lower() == 'y':
        return True
    elif result.lower() == 'l':
        return "leave"
    elif result.lower() == 'c':
        return "close"
    return False

tabs_to_close = []
# here, we're asking the user to go through 5 tabs and mark them as either music or not music
# if enough tabs in a window are music tabs, we determine the window to be a music window
non_music_tabs = []

for window, count in youtube_windows.items():
    if count > sorting_limit:
        if music_window: # music window already found, this is a non-music window
            large_windows[window] = count
            continue
        # let's check if this is a music window!
        print("Large window {} has {} tabs".format(repr(window), count))
        non_music_tabs = []
        for i in range(music_tabs_to_check):
            tab = random.choice(common.filter_tabs_by_window(tabs, window))
            # avoid repetitions
            while tab in non_music_tabs:
                tab = random.choice(common.filter_tabs_by_window(tabs, window))
            result = ask_if_music_tab(tab)
            if result == "close":
                tabs_to_close.append(tab)
            elif result:
                # we're not filtering music tabs from non-music windows yet
                pass #music_tabs.append(tab)
            else:
                non_music_tabs.append(tab)
        # we've checked some tabs, now let's see if it's likely that the window is a music window
        if music_tabs_to_check-len(non_music_tabs) >= music_tab_threshold:
            # this is the music window
            music_window = window
        else:
            large_windows[window] = count

for tab in tabs_to_close:
    print("Closing tab {}".format(tab.get_full_id()))
    cl.close_tabs([tab.get_full_id()])

tabs_to_close = []

if music_window is None:
    print("Music window not found! Sorting can't proceed")

largest_window = max(large_windows.items(), key=operator.itemgetter(1))[0]

# first, moving any manually-found non-music tabs from the music window into the largest window
# wouldn't want to just leave them in the music window
old_tabs = common.serialize_tabs(tabs)
for tab in non_music_tabs:
    print("Moving non-music tab {} from window {} to window {}".format(tab.get_full_id(), tab.window, largest_window))
    tab.window = largest_window
new_tabs = common.serialize_tabs(tabs)
common.update_tabs(cl, old_tabs, new_tabs)

# regenerate all the variables we'll be using
tabs = common.parse_tabs(cl)
youtube_tabs = [tab for tab in tabs if "youtube.com" in tab.url]

# merge all large non-music windows together with the largest window

for window in large_windows:
    if window == largest_window:
        break
    # this is currently impossible with the windows I have open
    #print("Processing a large window - this cannot be!")
    #import pdb; pdb.set_trace()
    old_tabs = common.serialize_tabs(tabs)
    window_tabs = common.filter_tabs_by_window(tabs, window)
    for tab in window_tabs:
        print("Moving tab {} from window {} to window {}".format(tab.get_full_id(), tab.window, largest_window))
        tab.window = largest_window
    new_tabs = common.serialize_tabs(tabs)
    # this code recalculates the tab indices and also calls the move command
    common.update_tabs(cl, old_tabs, new_tabs)
    tabs = common.parse_tabs(cl)

other_windows = [window for window in youtube_windows.keys() if window not in large_windows and window != music_window]

if other_windows:
    print("Other windows: {}".format(other_windows))
else:
    print("Sorting finished, no small windows found!")
    import sys;sys.exit(0)

# now, prompting the user to sort through small windows one-by-one

old_tabs = common.serialize_tabs(tabs)
for window in other_windows:
    window_tabs = common.filter_tabs_by_window(tabs, window)
    for tab in window_tabs:
        if tab not in youtube_tabs:
            continue
        result = ask_if_music_tab(tab, leave_option = True)
        do_leave = result is None
        if result == "leave":
            continue
        elif result == "close":
            tabs_to_close.append(tab)
            continue
        elif result:
            destination = music_window
        else:
            destination = largest_window
        print("Moving tab {} from window {} to window {}".format(tab.get_full_id(), tab.window, destination))
        tab.window = destination

for tab in tabs_to_close:
    print("Closing tab {}".format(tab.get_full_id()))
    cl.close_tabs([tab.get_full_id()])

new_tabs = common.serialize_tabs(tabs)
common.update_tabs(cl, old_tabs, new_tabs)

print("Sorting finished!")
