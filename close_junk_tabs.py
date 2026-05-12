from common import *
import vars
import sys

cl = get_client()
tabs = parse_tabs(cl)

def small_window_interactive_cleanup(used_windows):
    #main_window = used_windows[0]
    tabs = parse_tabs(cl)
    for tab in list(reversed(tabs)):
        if tab.window not in used_windows:
            print(f"{tab.name} ( {tab.url} )")
            if is_empty_tab(tab):
                print("Closing {} in window {}".format(tab.url, tab.window))
                cl.close_tabs([tab.get_full_id()])
                continue
            action = ask_tab_action("What do?", answers=["[s]kip", "[l]eave", "[c]lose", "[q]uit"])
            if action == "skip":
                break
            elif action == "leave":
                continue
            elif action == "close":
                print("Closing {} in window {}".format(tab.url, tab.window))
                cl.close_tabs([tab.get_full_id()])
            elif action == "quit":
                sys.exit(0)

# closing all "close on sight" tabs

for tab in tabs:
    if any([fn(tab) for fn in vars.junk_just_close]):
        print("closing tab", tab.url)
        cl.close_tabs([tab.get_full_id()])

tabs = parse_tabs(cl)

for tab in list(reversed(tabs)):
    if any([fn(tab) for fn in vars.junk_ask_for_action]):
        print(f"{tab.name} ( {tab.url} )")
        action = ask_tab_action("What do?", answers=["[s]kip", "[l]eave", "[c]lose", "[q]uit"])
        if action == "leave":
            continue
        elif action == "skip":
            break
        elif action == "close":
            print("Closing {} in window {}".format(tab.url, tab.window))
            cl.close_tabs([tab.get_full_id()])
        elif action == "quit":
            sys.exit(0)

