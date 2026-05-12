export_youtube_out_file = 'FILEOFYOURCHOICE'
save_bsky_target_dir = 'DIROFYOURCHOICE'
save_discord_target_dir = 'DIROFYOURCHOICE'

junk_just_close = [
  lambda tab: tab.url.endswith("lcsc.com/"),
  lambda tab: "lcsc.com/datasheet/" in tab.url,
  lambda tab: tab.url.startswith("https://bsky.app/profile/trending.bsky.app/feed/"),
]

bsky_profile_marker = "https://bsky.app/profile/"

junk_ask_for_action = [
  lambda tab: tab.url.startswith("https://duckduckgo.com/"),
  lambda tab: tab.url.startswith("https://bsky.app/search?"),
  # check for url being a bsky profile (doesn't have any / in it after the profile part is cut off
  lambda tab: tab.url.startswith(bsky_profile_marker) and "/" not in tab.url[len(bsky_profile_marker):],
]
