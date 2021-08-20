import asyncio
import os
import random
import re
import bs4
import requests
import httpx
import aiofiles
import time


class Parsing:

    def __init__(self):
        self.ips = str(random.randint(1, 255)) + "." \
                   + str(random.randint(1, 255)) + "." \
                   + str(random.randint(1, 255)) + "." \
                   + str(random.randint(1, 255))

    # 获取每个子页面的数据
    def parsing(self, url):
        agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92."
                               "0.4515.107 Safari/537.36",
                 "X-Forwarded-For": self.ips
                 }
        response = requests.get(url, headers=agent).content
        return response

    # 获取子页面的<a>标签，就可以获取每个主题的链接
    def parsing_a(self, response):
        soup = bs4.BeautifulSoup(response, "html.parser").find_all("a")
        link = re.findall(r"https://zazhitaotu.cc/archives/[0-9]*.html", str(soup))
        return link

    # 获取页面的所有<img>标签，并且用 re 模块解析出.jpg 的链接
    def parsing_img(self, link):
        soup = bs4.BeautifulSoup(link, "html.parser").find_all("img")
        img_url = re.findall(r"(h\S*?jpg)", str(soup))
        return img_url

    async def download(self, url, path):
        try:
            filename = url.split("/")[-1]
            async with httpx.AsyncClient() as client1:
                response = await client1.get(url)
                async with aiofiles.open(path + filename, "wb+") as f:
                    await f.write(response.content)
        except Exception:
            print("下载失败，请求频率过高")


async def main():
    page = [f"https://zazhitaotu.cc/page/{url}/" for url in range(1, 26)]
    x = Parsing()
    for i in page:
        page_url = x.parsing(i)
        a_url = x.parsing_a(page_url)
        for url in a_url:
            img_url = x.parsing(url)
            name = bs4.BeautifulSoup(img_url, "html.parser").find("title").string
            jpg_link = x.parsing_img(img_url)
            path = "./zazhitaotu.cc/" + name + "/"
            try:
                os.makedirs(path)
            except Exception:
                print("文件存在")
                continue
            print("下载完毕{}".format(name))
            task_list = [asyncio.create_task(x.download(i, path)) for i in jpg_link]
            time.sleep(1)
            await asyncio.wait(task_list)
             
                
if __name__ == '__main__':
    t1 = time.time()
    asyncio.run(main())
    print("全部下载完毕")
    print(time.time() - t1)
