import requests
from bs4 import BeautifulSoup

import os
import pprint
import time
import urllib.error
import urllib.request

# PDF
import img2pdf
from PIL import Image # img2pdfと一緒にインストールされたPillowを使います

"""
Refs:
    * https://lightgauge.net/language/python/8702/
    * https://qiita.com/sqrtxx/items/49beaa3795925e7de666#%E7%94%BB%E5%83%8F
    * https://www.it-swarm-ja.com/ja/image/python-urllib%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6url%E3%81%8B%E3%82%89%E7%94%BB%E5%83%8F%E3%82%92%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89%E3%81%99%E3%82%8B%E3%81%8C%E3%80%81http%E3%82%A8%E3%83%A9%E3%83%BC403%E3%82%92%E5%8F%97%E4%BF%A1%E3%81%99%E3%82%8B%EF%BC%9A%E7%A6%81%E6%AD%A2/823004869/
    * https://note.nkmk.me/python-download-web-images/
    * https://techacademy.jp/magazine/26426
    * https://gammasoft.jp/support/pip-install-error/ (pip installでエラーになりインストールできない場合（Windows）)
    * https://www.python.jp/install/windows/install.html (Windows版Pythonのインストール)
    * https://pythonlinks.python.jp/ja/index.html (非公式Pythonダウンロードリンク)
    * https://pip.pypa.io/en/stable/installing/ (pip documentation v21.1.2)
    * https://qiita.com/neet-AI/items/98d4194872ee4f53e3b4#%E7%B7%8F%E9%9B%86%E7%B7%A8 (Pythonで画像スクレイピングをしよう)
    * 
"""

NAME_LIST = [
    ("sanple", 1, 5, "https://mumvall.com")

]

PATH_TEMP = "C:\\"

def download_file(img_url, ref_url, title, ua, dst_path):
    """
    pick up file name from the url
    Args:
        img_url:    string: url (end to '.img' or 'png')
        ref_url:    string: url
        title:      int:    epsode
        ua:         user agent
        dst_path:   path to destination
    """
    try:
        req = urllib.request.Request(img_url,headers={'User-agent': ua,'referer':ref_url})
        with urllib.request.urlopen(req) as web_file:
            data = web_file.read()
            # zero padding
            # refs: https://note.nkmk.me/python-zero-padding/
            zp_title = title.zfill(4)
            # https://note.nkmk.me/python-os-mkdir-makedirs/
            os.makedirs(dst_path + "/" + zp_title + "/", exist_ok=True)
            file_path = dst_path + "/" + zp_title + "/" + pickFileNameFromUrl(img_url)
            with open(file_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)
        pass
    except Exception as e:
        print("例外args:", e.args)
        pass


def pickFileNameFromUrl(url):
    """
    pick up file name from the url
    Args:
        url:    string: url
    """
    if len(url) <= 0:
        return "nanashisan"
    list = url.split("/")
    return list[len(list)-1]

def imgInUrl_(url, ua, ep, dest_path):
    """
    get images from the url
    Args:
        url:    string: url for getting
        ua:     user agent
        ep:     episode
        dest_path: path to destination
    Refs:
        https://lightgauge.net/language/python/8702/
    """
    # https://qiita.com/neet-AI/items/98d4194872ee4f53e3b4#%E7%B7%8F%E9%9B%86%E7%B7%A8
    response = requests.get(url,headers={'User-agent': ua,'referer':url})
    soup = BeautifulSoup(response.text,'lxml')

    # タイトルの取得
    title = soup.title.string
    print(title)

    # リンクの取得
    links = soup.findAll('img')
    for link in links:
        img_url = link.get('data-src')
        if img_url != None:
            download_file(img_url, url, str(ep), ua, dest_path)

def imgInUrl(url, ep, dest_path):
    """
    get images from the url
    Args:
        url:    string: url for getting
        ep:     episode
        dest_path: path to destination
    Refs:
        https://lightgauge.net/language/python/8702/
    """
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
     'AppleWebKit/537.36 (KHTML, like Gecko) '\
     'Chrome/55.0.2883.95 Safari/537.36 '
    return imgInUrl_(url, ua, ep, dest_path)

def convertPDF(name, ep, dir):
    ep = ep.zfill(4)
    saveDir = dest_path + "\\話別PDF"
    os.makedirs(saveDir, exist_ok=True)

    fileName = "{}_ep.{}.pdf".format(name, ep)
    extension  = ".jpg"

    layout_pdf = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))

    with open(saveDir + "\\" + fileName,"wb") as f:
        # 画像フォルダの中にあるファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(img2pdf.convert([Image.open(dir + "\\" + j).filename for j in os.listdir(dir) if j.endswith(extension)], layout_fun=layout_pdf))

def allinone(name, ep_from, ep_to, url, dest_path):
    # 各URLごとに画像を取得
    for idx in range(ep_from, ep_to + 1):
         url_item = url.format(idx)
         imgInUrl(url_item, idx, dest_path)

    for idx in range(ep_from, ep_to + 1):
        dir_ = dest_path  + "\\" + str(idx).zfill(4)
        print(dir_)
        convertPDF(name, str(idx), dir_)

try:
    for name, ep_from, ep_to, url in NAME_LIST:
        dest_path = PATH_TEMP.format(name)
        #print(ep_from, ep_to, url, dest_path)
        allinone(name, ep_from, ep_to, url, dest_path)
except Exception as e:
    print("例外args:", e.args)
    pass