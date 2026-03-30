from common import *
import sys

cl = get_client()
tabs = parse_tabs(cl)

def small_window_interactive_cleanup(used_windows):
    #main_window = used_windows[0]
    tabs = parse_tabs(cl)
    for tab in tabs:
        if tab.window not in used_windows:
            print(f"{tab.name} ( {tab.url} )")
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

# closing all LCSC datasheet tabs

current_tabs = [tab for tab in tabs if ("lcsc.com/datasheet/") in tab.url]
if not current_tabs:
    print("No LCSC datasheets open")

for tab in current_tabs:
    print("Closing LCSC datasheet tab in window {}".format(tab.window))
    cl.close_tabs([tab.get_full_id()])


common_domains = [
  "lcsc.com/",
]

current_tabs = [tab for tab in tabs if any([tab.url.endswith(url) for url in common_domains])]
if not current_tabs:
    print("No common homepages found")

for tab in current_tabs:
    print("Closing {} in window {}".format(tab.url, tab.window))
    cl.close_tabs([tab.get_full_id()])

ask_before_domains = [
  "https://bsky.app/search?",
]


current_tabs = [tab for tab in tabs if any([tab.url.startswith(domain) for domain in ask_before_domains])]
if not current_tabs:
    print("No ask-before-closing windows found")

for tab in current_tabs:
    print(f"{tab.name} ( {tab.url} )")
    action = ask_tab_action("What do?", answers=["[l]eave", "[c]lose", "[q]uit"])
    if action == "leave":
        continue
    elif action == "close":
        print("Closing {} in window {}".format(tab.url, tab.window))
        cl.close_tabs([tab.get_full_id()])
    elif action == "quit":
        sys.exit(0)
    #s = "{} - '{}' ({}:{}), from {}".format(tab.url, name, duration_m, duration_s, tab.sinfo.get("uploader", "[UNKNOWN]"))
