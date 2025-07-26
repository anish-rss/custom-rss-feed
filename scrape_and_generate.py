import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

URL = "https://newalbumreleases.net/category/cat/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")
posts = soup.select("div.post")

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "New Album Releases – CAT"
ET.SubElement(channel, "link").text = URL
ET.SubElement(channel, "description").text = "Custom feed for the CAT category"

for post in posts[:10]:
    a_tag = post.select_one("h2 a")
    title = a_tag.text.strip()
    link = a_tag["href"]
    pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    ET.SubElement(item, "pubDate").text = pub_date
    ET.SubElement(item, "description").text = f"New album: {title}"

ET.ElementTree(rss).write("feed.xml", encoding="utf-8", xml_declaration=True)
