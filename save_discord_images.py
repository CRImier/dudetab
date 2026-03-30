import traceback
import requests
import shutil
import os

from common import *

target_dir = 'DIROFYOURCHOICE'

from zpui_lib.helpers import get_safe_file_backup_path

cl = get_client()
tabs = parse_tabs(cl)

discord_tabs = [tab for tab in tabs if "https://cdn.discordapp.com/attachments/" in tab.url or "https://media.discordapp.net/attachments/" in tab.url]

for tab in discord_tabs:
    last_part = tab.url.rsplit('/', 1)[-1]
    print(last_part)
    filename = last_part.rsplit('?', 1)[0]
    print(filename)
    path = os.path.join(target_dir, filename)
    print(tab.url)
    print(filename)
    if os.path.isfile(path):
        current_path, new_path = get_safe_file_backup_path(target_dir, filename)
        print("Path {} already has a file; using {} instead".format(current_path, new_path))
        path = new_path
    try:
        rqq = requests.get(tab.url, stream=True)
        if rqq.status_code != 200:
            print("Can't download from URL {}: code {}! {}".format(tab.url, rqq.status_code, repr(tab.id)))
            cl.close_tabs([tab.get_full_id()])
            continue
        rqq.raw.decode_content = True
        with open(path, 'wb') as f:
            shutil.copyfileobj(rqq.raw, f)
        print("Downloaded URL {}!".format(tab.url))
    except:
        print("Can't download from URL {}!".format(tab.url))
        traceback.print_exc()
        print(tab.id)
        cl.close_tabs([tab.get_full_id()])
    else:
        cl.close_tabs([tab.get_full_id()])

