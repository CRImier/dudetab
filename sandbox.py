from common import *

cl = get_client()
tabs = parse_tabs(cl)
windows = get_window_ids(tabs)

print(len(tabs))
