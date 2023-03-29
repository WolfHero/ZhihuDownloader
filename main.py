import requests
import os

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("未安装必要的BeautifulSoup库\n"
          "选择预期的Python后环境输入下面的语句进行安装\n"
          "pip install bs4 -i https://pypi.douban.com/simple --trusted-host pypi.douban.com"
          "pip install lxml -i https://pypi.douban.com/simple --trusted-host pypi.douban.com")
    exit()

print(" 知乎回答下载器 | 离线收藏你喜爱的")
print("      Made By WolfHero")
print("----------------------------")
while True:
    n = input("是否盐选内容？输入[Y]es/[N]o：\n")
    if n in ['Y', 'y', 'Yes', 'yes']:
        filename = input(
            "盐选内容需要会员登录后先按Ctrl+S保存网页，再将网站拖入此处以输入网页绝对路径：\n"
            "如果你用的是旧版命令提示符或者Pycharm运行此脚本，可能会遇到拖拽文件操作无反应的现象，建议按住Shift右键网页文件，然后点击菜单中的复制文件地址~\n")
        if '"' in filename:
            filename = filename.strip('"')
        if os.path.exists(filename):
            url = [0, filename]
            break
    elif n in ['N', 'n', 'No', 'no']:
        link = input("非盐选内容输入回答链接即可下载：")
        if 'zhihu.com' in link:
            url = [1, link]
            break
    print("输入有误")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/111.0.0.0 Safari/537.36'}
if url[0]:
    html = requests.get(url=url[1], headers=headers).content.decode('utf-8')
else:
    html = open(url[1], encoding='utf-8')
site = BeautifulSoup(html, 'lxml')
title = site.find_all('meta', attrs={'itemprop': "name"}, recursive=True, limit=1)[0].__getattribute__('attrs')[
    'content']
url = site.find_all('meta', attrs={'itemprop': "url"}, recursive=True, limit=1)[0].__getattribute__('attrs')['content']
keywords = site.find_all('meta', attrs={'itemprop': "keywords"}, recursive=True, limit=1)[0].__getattribute__('attrs')[
    'content']
author = site.find_all('div', attrs={'class': 'AuthorInfo'}, limit=1)[0].find_next('meta', attrs={
    'itemprop': "name"}).__getattribute__('attrs')['content']
print("问题名：" + title + "\n问题关键词：" + keywords + "\n回答作者名：" + author + "\n回答链接：" + url)
print("\n===============正文===============\n")
text = site.find('div', attrs={'class': "RichContent-inner"})
for i in text:
    if i.text.find('.css') == -1:
        print(i.text)

with open(title + ".txt", mode="wt+", encoding="utf-8") as f:
    f.write("问题名：" + title + "\n问题关键词：" + keywords + "\n回答作者名：" + author + "\n回答链接：" + url)
    f.write("\n===============正文===============\n")
    for i in text:
        if i.text.find('.css') == -1:
            f.write(i.text)

print("下载完成，文件名为：”" + title + ".txt“")
if not url[0]:
    html.close()
