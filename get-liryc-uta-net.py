import re
import sys

import requests
from bs4 import BeautifulSoup

def get_lyric(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features="html.parser")
    lyrics = soup.find(id="kashi_area").get_text("\n")
    title = soup.find(class_="blur-filter").find("h2").get_text()
    author = soup.find(class_="blur-filter").find("span").get_text()
    tmp = soup.find(class_="blur-filter").find_all("p")
    if len(tmp) > 1:
        published = tmp[1].get_text()
    else:   
        published = tmp[0].get_text()
    published = re.findall("\d\d\d\d\/\d\d\/\d\d", published)
    published = published[0] if published else ""
    return lyrics, title, author, published

def get_lyric_list(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features="html.parser")
    lyric_list_table = soup.find_all(class_="songlist-table-body")
    lyrics = []
    for lyric_list in lyric_list_table:
        lyrics_row = lyric_list.find_all("tr")
        for lyric_row in lyrics_row:
            a = lyric_row.find_all("td")[0].find("a")
            url = "https://uta-net.com" + a.get("href")
            title = a.find("span").get_text()
            lyric = lyric_row.find_all("td")[5].find("span").get_text()
            lyrics.append({
                "url": url,
                "title": title,
                "lyric": lyric,
            })
    return lyrics


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please input uta-net URL.")
        print("example: https://www.uta-net.com/artist/9867/")
        exit(1)
    url = sys.argv[1]
    lyrics =  get_lyric_list(url)

    # 歌詞を保存する
    for lyric in lyrics:
        url, title, lyric = lyric.values()
        _, _, _, published = get_lyric(url)
        with open(f"./lyrics/{title}.txt", "w", encoding="utf-8") as f:
            f.write(title + "\n")
            f.write(published + "\n")
            f.write(lyric)
