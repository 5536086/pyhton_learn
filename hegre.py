import os
import re
import requests
import bs4


def open_cookie():
    with open("hegre.cookie") as f:
        file = f.read()
        cookie = file.strip("\n")
        return str(cookie)


cookie = open_cookie()
agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92."
                       "0.4515.107 Safari/537.36",
         "Cookie": cookie
         }


# 获取作者的所有图集作品，返回一个列表
def parsing_author(url):
    x = requests.get(url, headers=agent).content
    soup = bs4.BeautifulSoup(x, "html.parser")
    # 解析出作者图集的 div 区块
    photo_block = soup.find_all(attrs={"id": "galleries-listing"})
    photo_link = re.findall(r"href=\"(/photos/.*?)\"", str(photo_block))
    photo_link_list = ["https://www.hegre.com" + url for url in photo_link]
    return photo_link_list


# 获取子页面中压缩包的下载地址
def parsing_page(url):
    x = requests.get(url, headers=agent).content
    soup = bs4.BeautifulSoup(x, "html.parser").find_all(attrs={"class": "gallery-zips"})
    link_zip = re.findall(r"href=\"(.*?)\"", str(soup))
    # 只返回 4K 的下载链接
    return link_zip[0]


def download(url, path):
    zip_url = requests.get(url, headers=agent).content
    filename = url.split("/")[-1]
    with open(path + filename.split("?")[0], "wb+") as f:
        f.write(zip_url)


def main(url):
    author = url.split("/")[-1]
    # path = "/你自己想要保存的地址/hegre" + "/" + author + "/"
    path = "hegre" + "/" + author + "/"
    try:
        os.makedirs(path)
        print("创建文件夹成功，开始下载", end="")
    except Exception:
        print("文件夹存在，无需创建，开始下载", end="")
    x = parsing_author(url)
    total = len(x)
    num = 0
    for i in parsing_author(url):
        num += 1
        t = num / total * 100
        print("\r", end="")
        print("Download Progress [{}%]:".format(int(t)), "=" * (int(t) // 2), end="")
        download(parsing_page(i), path)


if __name__ == "__main__":
    try:
        main("https://www.hegre.com/models/" + input("作者名字（作者链接的最后一个字段，比如：kiki，emily）："))
    except KeyboardInterrupt:
        print("\n感谢使用 👋")
