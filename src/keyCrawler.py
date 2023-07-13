import re
from bs4 import BeautifulSoup
from logging import Logger
from selenium import webdriver


def crawlYoutubeKey(song_id: str, song_title: str, artist: str, query_url: str, log: Logger) -> dict:
    log.info("- Crawling Youtube Key of Song ID : %s", song_id)
    song_title = re.sub(" ", "+", song_title)
    artist = re.sub(" ", "+", artist)
    link = f"{query_url}{artist}%22+%22{song_title}%22"

    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    op.add_argument("disable-gpu")
    op.add_argument("incognito")
    op.add_argument("--blink")

    driver = webdriver.Chrome(options=op)
    driver.get(url=link)
    # driver.implicitly_wait(1)
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    data = soup.find(class_="yt-simple-endpoint style-scope ytd-video-renderer")

    video_url = data["href"]

    start_idx = video_url.find("v=")
    end_idx = video_url.find("&pp")
    key = video_url[start_idx + 2 : end_idx]

    log.info("- Youtube Key : %s", key)

    return {"SONG_ID": song_id, "YOUTUBE_KEY": key}
