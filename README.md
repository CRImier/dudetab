# dudetab
Scripts using brotab's Python API to do useful things

Sorted by increasing complexity:

* ```close_youtube_home_tabs.py``` - closes all YouTube homepage tabs (tabs with the "https://youtube.com" URL)
* ```close_empty_windows.py``` - closes windows only containing empty tabs
* ```move_to_new_tabs.py``` - for each window where a "heavy" tab is currently active, either moves to an empty tab in the same window or opens an empty tab in that window. This helps reduce memory consumption after a Firefox session is restored.
* ```aggregate_bsky_tabs.py``` - closes all Bluesky timeline tabs and moves Bluesky tabs from all windows into a window that contains the most Bluesky tabs
* ```aggregate_youtube_tabs.py``` - closes all YouTube main page tabs. Then, allows the user to sort all YouTube tabs into two windows - one with regular YouTube videos and one with YouTube music videos, so that, in the end, there's only two windows left containing YouTube tabs.
* ```aggregate_youtube_tabs_simpl.py``` - closes all YouTube main page tabs. Then, puts all the YouTube tabs into the window that contains the most YouTube tabs pre-sorting.
* ```export_youtube_tabs.py``` - closes all YouTube main page tabs. Then, fetches metadata for all open YouTube video tabs using `yt-dlp`. Then, lets you sort through the tabs to either close them, ignore them, or append the video URL&name&channel to a text file of your choice. Also lets you quit the script mid-sorting in case you get tired midway.
* ```sandbox.py``` - is a sandbox for you to play with brotab. Run it as `python -i sandbox.py` and get an interactive shell with important variables populated (run `dir()` for introspection).
* ```save_bsky_images.py``` - downloads all open `cdn.bsky.app` tabs into a folder of your choosing, then closes the tabs with successfully downloaded content.
* ```save_discord_images``` - downloads all open `cdn.discordapp.com` tabs into a folder of your choosing, then closes the tabs with successfully downloaded content. Run it like every 12 hours, since in their infinite wisdom, Discord puts a 24h expiration on those URLs.
* ```aggregate_tabs.py``` - a mega-script that runs a lot of the scripts above, and then sorts all open tabs into 4 windows (main, youtube, bluesky, and catch-all for everything else). Afterwards, it deduplicates about:newtab windows. Will do more deduplication later on. Should also integrate `move_to_new_tabs.py` at some point.
* ```close_junk_tabs.py``` - a small mostly-tailored script that closes a bunch of useless tabs; some of them it can ask about. add your own tabs and mod the script as you see fit!

Other files:
* ```heavy_tab_hosts.txt``` - list of "heavy" hosts for the ```move_to_new_tabs.py``` script
* ```common.py```: common helper functions

Run with Python 3. Run these scripts as ```python3 -i script.py``` to get a commandline you can further experiment in after the script stops running.
