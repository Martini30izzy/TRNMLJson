import json
import requests
import feedparser
from datetime import datetime
from zoneinfo import ZoneInfo

# -----------------------------------
# CHANNEL IDS
# -----------------------------------

CHANNEL_IDS = [
 'UCuFFtHWoLl5fauMMD5Ww2jA',  #1 CBC News
    'UC85rJiWmYQV8Shk3QWXT8MQ',  #2 The Chrome Project
    'UC94CRUtB0q7U8-67qrT37fA',  #3 Vancini Conversions
    'UCL_BZpt0J9Kqwy6YPWr30ow',  #4 Mav
    'UCOgGAfSUy5LvEyVS_LF5kdw',  #5 JOLLY
    'UCHHqGs3reVzjf7LmC5F4ltA', #6 Star Wars: Tales Untold
    'UCZYXO1yZnSAT6sK79bZV_Hg', #7 RyanTwomey
    'UCauITualRcxWe3tmUNUSLGQ', #8 The Mark Ellis Tech Diary
    'UCwwuSBYcErVlOpveYubHv4g', #9 Mark Ellis Reviews
    'UC9GdeF0na1YQhqGRLTp7UpA', #10 Nothing Epic
    'UCDiFRMQWpcp8_KD4vwIVicw', #11 Emergency Awesome
    'UC16niRr50-MSBwiO3YDb3RA', #12 BBC News
    'UChME7blpRpX1ViN-oPBpNmw', #13 Zeliha Akpinar
    'UCyXD1jAZBdZ4u0K-GLYC77Q', #14 Movie Recaps
    'UC5OdB-sGz9atv-tJINwWOTg', #15 Ambition Strikes
    'UCBJycsmduvYEL83R_U4JriQ', #16 Marques Brownlee
    'UCaffuWQ2mLfRevosyKoz87Q', #17 Zach Highley
    'UCPD_bxCRGpmmeQcbe2kpPaA', #18 First We Feast
    'UCasvDNJLIODOEO1YBNKBnGQ', #19 the exPAWers
    'UCNZMOOmPJStgwhiJ3x-MZ_A', #20 Marvelous Videos
    'UCwBV-eg1dAkzrdjqJfyEj0w', #21 MovieGasm‍․com
    'UCpogf2vVFqIHrj5G9MsWotg', #22 The cat lady VAN
    'UCiKE6mqbKmGGlNAtccn04MA', #23 CBC British Columbia
    'UCCqEeDAUf4Mg0GgEN658tkA', #24 Chris Stuckmann
    'UCLRlryMfL8ffxzrtqv0_k_w', #25 KinoCheck.com
    'UC1cVTv6C0Unv6TtadjBvYRA', #26 Rapid Trailer
    'UCHJy1RypctP_ozyxaLTXlBg', #27 Tiny Cabin Life
    'UCyjbXgCB8MVJR7ySvwR-wRg', #28 GateWorld
    'UCDWYbhR94ZYFUXd4NJvAHYQ', #29 Kit Betts-Masters
    'UCWKveACEz1euuOk5eyzzvTg', #30 Tick Talk w/ Eric Migicovsky
    'UCOmcA3f_RrH6b9NmcNa4tdg', #31 CNET
    'UCYFQ33UIPERYx8-ZHucZbDA', #32 Apple Support
    'UC1Myj674wRVXB9I4c6Hm5zA', #33 Apple TV
    'UCNA9mfinVMxNJ8vaas8WRAQ', #34 All Recaps
    'UCirKiNvBJNHhdOIkFigKCjQ', #35 Skywalker Stories
    'UC_sEUZX3bh3PYkli3aRbIUg', #36 ARMAX
    'UCSNAOq33nv3Ifd6q3b6lKbg', #37 Solar Power Edge
    'UCvdt3dIKwo3CCp6U5nXCFWA', #38 Ethan Liebross
    'UCtWMBrBGnMLtVj5JfT2E13Q', #39 FishN More
    'UCpSgg_ECBj25s9moCDfSTsA', #40 Jamie Olivier - remove if get too many
    'UCcE10s4MFy4eed7q7QkonZg', #41 First to Eleven - remove if get too many
    'UCQhHCq1Xyj3pVEx1ebf49HQ', #42 Movies And Munchies
    'UCHhy08xelXhKIOwgsFssaTQ', #43 Good e-Reader
    'UCivi_f1nniBzEOfKhRoN12Q', #44 Grind Hard Plumbing Co
    'UCSOpcUkE-is7u7c4AkLgqTw', #45  MrMobile [Michael Fisher]
    'UCDYJ3BCFTGLylzCtKTrlkMw', #46 That Mark Gilroy
    'UCVLN0tY51ewH44wUtx3YZTA', #47 Tech Sprut
    'UCErmMCK1sHF-kCtyHpuSXtQ', #48 Mark Kermode reviews

]

headers = {
    "User-Agent": "Mozilla/5.0"
}

videos = []

for channel_id in CHANNEL_IDS:

    try:

        rss_url = (
            f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        )

        r = requests.get(
            rss_url,
            headers=headers,
            timeout=20
        )

        feed = feedparser.parse(r.text)

        if len(feed.entries) == 0:
            continue

        entry = feed.entries[0]

        video_id = entry.get("yt_videoid", "")

        image_url = (
            f"https://img.youtube.com/vi/{video_id}/default.jpg"
        )

        published = entry.get("published", "")

        try:
            dt = datetime.fromisoformat(
            published.replace("Z", "+00:00")
            )

            dt = dt.astimezone(
            ZoneInfo("America/Vancouver"))
         
            # published = dt.strftime("%b %d %H:%M")
            published = dt.strftime("%b %d %H:%M %Z")

        except Exception:
            pass

        videos.append({
            "t": entry.get("title", "")[:60],
            "c": entry.get("author", "")[:22],
            "i": image_url,
            "d": published
        })

        print("Added:", entry.get("author", ""))

    except Exception as e:
        print("ERROR:", channel_id, e)

payload = {
   # "last_updated": datetime.now().strftime("%H:%M"),
    "last_updated": datetime.now(
         ZoneInfo("America/Vancouver")
         ).strftime("%H:%M"),
    "page1": videos[:24],
    "page2": videos[24:48]
}

with open("youtube.json", "w") as f:
    json.dump(payload, f, indent=2)

print("")
print("Generated youtube.json")
print("Videos:", len(videos))

