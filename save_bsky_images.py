import traceback
import requests
import shutil
import os

from common import *
import vars

target_dir = vars.save_bsky_target_dir


cl = get_client()
tabs = parse_tabs(cl)

bsky_tabs = [tab for tab in tabs if "https://cdn.bsky.app" in tab.url]

for tab in bsky_tabs:
    last_part = tab.url.rsplit('/', 1)[-1]
    print(last_part)
    if not '@' in last_part:
        print("Can't find @ in ", tab.url)
        last_part += "@webp" # hack hehe
    fn, ext = last_part.rsplit('@', 1)
    filename = fn+'.'+ext
    print(filename)
    path = os.path.join(target_dir, filename)
    if os.path.isfile(path):
        print("Path {} already has a file; closing".format(path))
        cl.close_tabs([tab.get_full_id()])
        continue
    try:
        rqq = requests.get(tab.url, stream=True)
        if rqq.status_code != 200:
            print("Can't download from URL {}: code {}!".format(tab.url, rqq.status_code))
            continue
        rqq.raw.decode_content = True
        with open(path, 'wb') as f:
            shutil.copyfileobj(rqq.raw, f)
        print("Downloaded URL {}!".format(tab.url))
    except:
        print("Can't download from URL {}!".format(tab.url))
        traceback.print_exc()
    else:
        cl.close_tabs([tab.get_full_id()])
