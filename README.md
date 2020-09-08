# dudetab
Scripts using brotab's Python API to do useful things

* ```aggregate_twitter_tabs.py``` - closes all Twitter timeline tabs and moves Twitter tabs from all windows into a window that contains the most Twitter tabs
* ```close_empty_windows.py``` - closes windows only containing empty tabs
* ```move_to_new_tabs.py``` - for each window where a "heavy" tab is currently active, either moves to an empty tab in the same window or opens an empty tab in that window. This helps reduce memory consumption after a Firefox session is restored.
* ```heavy_tab_hosts.txt``` - list of "heavy" hosts for the ```move_to_new_tabs.py``` script
* ```common.py```: common helper functions
