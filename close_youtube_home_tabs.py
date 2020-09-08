import common

cl = common.get_client()
tabs = common.parse_tabs(cl)

# closing all YouTube homepage tabs - tabs with "https://youtube.com/" URL

youtube_home_tabs = [tab for tab in tabs if tab.url.endswith("youtube.com/")]

for tab in youtube_home_tabs:
    print("Closing YouTube home tab in window {}".format(tab.window))
    cl.close_tabs([tab.get_full_id()])
