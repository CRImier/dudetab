from brotab import main as btm
from brotab import api as brapi

default_browser = "firefox"

def get_client(requested_browser = None):
    if requested_browser is None:
        requested_browser = default_browser
    clients = btm.create_clients()
    if not clients:
        raise Exception("No clients found!")
    browser_matches = [cl for cl in clients if cl._get_browser() == requested_browser]
    if not browser_matches:
        raise Exception("No clients found!")
    if len(browser_matches) > 1:
        # use the last client
        print("Too many clients found, don't know what to do! Picking the last one", browser_matches)
    return browser_matches[-1]


class Tab():
    def __init__(self, prefix, window, id, name, url):
        self.prefix = prefix
        self.window = window
        self.id = id
        self.name = name
        self.url = url

    def get_full_id(self):
        return ".".join([self.prefix, self.window, self.id])

    def to_string(self):
        return "\t".join([self.get_full_id(), self.name, self.url])

    def __str__(self):
        return f"<common.Tab {self.prefix}.{self.window}.{self.id} at {hex(id(self))}, URL: {self.url}>"


def serialize_tabs(tabs):
    """
    converts a list of Tab objects into strings, as they were before parsing
    this can then be used in update_tabs
    """
    return [tab.to_string() for tab in tabs]

def update_tabs(client, old_tabs, new_tabs):
    """
    after moving tabs between windows, pass old and new serialized tabs here so that the changes can actually be applied
    tab indices need to be recalculated, that's done by the brotab API call
    """
    return brapi.MultipleMediatorsAPI(None)._move_tabs_if_changed(client, old_tabs, new_tabs)

def get_window_ids(tabs):
    """
    gets tab objects and returns a list of window IDs
    """
    window_ids = [tab.window for tab in tabs]
    window_ids = list(set(window_ids))
    return window_ids

def parse_tabs(client):
    """
    returns a list of Tab objects
    """
    tabs = client.list_tabs_safe(None)
    for i, tab in enumerate(tabs):
        tabs[i] = tab.split('\t')
    # sanity-check tab lengths after parsing - result should be {3}
    tab_list_lengths = set([len(tab) for tab in tabs])
    try:
        assert ( tab_list_lengths == {3})
    except AssertionError:
        faulty_tab_strs = [repr(tab) for tab in tabs if len(tab) != 3]
        faulty_tabs_str = ", ".join(faulty_tab_strs)
        raise ValueError("Tab info parsing problem! Tab list lengths after parsing: {}, faulty tabs: {}".format(repr(tab_list_lengths), faulty_tabs_str))
    for i, tab in enumerate(tabs):
        tab[1:1] = tab[0].split('.')
        tab.pop(0)
        tabs[i] = Tab(*tabs[i])
    return tabs

def is_empty_tab(tab):
    return tab.url == "about:newtab" or tab.url == "about:home" or tab.url == "about:blank"

def filter_tabs_by_window(tabs, window):
    return [tab for tab in tabs if tab.window == window]

FunniException = type("FunniException", (Exception,), {})

def ask_tab_action(message, answers = ["[l]eave", "[c]lose", "[q]uit"]):
    def get_letter(a):
        return a.split("]", 1)[0].split("[")[-1]
    def strip_answer(a):
        return ''.join([letter for letter in a if letter not in "[]"])

    answer_dict = {get_letter(a):strip_answer(a) for a in answers}
    #message = "Save tab?"
    #prompt = "[s]ave? [l]eave? [c]lose? [q]uit? >>> "
    prompt = "? ".join(answers) + "? >>> "
    print(message)
    result = None
    valid_options = "".join(answer_dict.keys())
    valid_options += valid_options.upper()
    while not result or (result not in valid_options or len(result) > 1):
        result = input(prompt)
    return answer_dict[result.lower()]
    """
    if result.lower() == 's':
        return "save"
    elif result.lower() == 'l':
        return "leave"
    elif result.lower() == 'c':
        return "close"
    elif result.lower() == 'q':
        return "quit"
    else:
        raise FunniException
    """



if __name__ == "__main__":
    client = get_client()
    tabs = parse_tabs(client)
