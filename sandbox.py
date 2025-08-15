import common

cl = common.get_client()
tabs = common.parse_tabs(cl)
windows = common.get_window_ids(tabs)

print(len(tabs))
