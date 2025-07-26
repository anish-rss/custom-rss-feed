import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE_URL = "https://newalbumreleases.net/category/cat/"
NUM_PAGES = 5

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "New Album Releases – CAT"
ET.SubElement(channel, "link").text = BASE_URL
ET.SubElement(channel, "description").text = "Custom feed for the CAT category"

for page in range(1, NUM_PAGES + 1):
    url = BASE_URL if page == 1 else f"{BASE_URL}?paged={page}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Updated selector for posts
    posts = soup.select("div#main div.post")

    for post in posts:
        h2 = post.find("h2")
        a_tag = h2.find("a") if h2 else None
        if not a_tag:
            continue

        title = a_tag.text.strip()
        link = a_tag["href"]
        pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = link
        ET.SubElement(item, "pubDate").text = pub_date
        ET.SubElement(item, "description").text = f"New album: {title}"

ET.ElementTree(rss).write("feed.xml", encoding="utf-8", xml_declaration=True)
