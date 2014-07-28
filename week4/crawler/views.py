from flask import Flask, render_template, request
from apps import app

import urllib
from bs4 import BeautifulSoup

@app.route('/', methods=['GET', 'POST'])
def get():
    return render_template("index.html")


@app.route("/crawl", methods=['GET', 'POST'])
def crawl():

    htmltext = urllib.urlopen('http://comic.naver.com/webtoon/list.nhn?titleId=186811&weekday=thu&page=' + request.form['page']).read()
    soup = BeautifulSoup(htmltext, from_encoding="utf-8")
    authors = []
    result = ""

    for tag in soup.select(".title"):
        authors.append(tag.get_text())
    for author in authors:
        result += author.encode('utf-8') + "<br>"

    return result
