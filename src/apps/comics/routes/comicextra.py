"""
/comicextra/s/<query>
{
    "name": "NAME",
    "cover": "COVER",
    "detail": "/comics/comicextra/d/ID",
    "id": ID
}
/comicextra/d/<id>
{
    "name": "NAME",
    "cover": "COVER",
    "summary": "SUMMARY",
    "status": "STATUS",
    "genres": []
    "id": ID,
    "chapters": [
        {
            "name": "NAME",
            "number": "NUMBER",
            "detail": "/comics/comicextra/d/ID/NUMBER"
        }
    ]
}
/comicextra/d/<id>/<number>
{
    "name": "NAME",
    "parent": "/comics/comicextra/d/ID",
    "images": []
}
"""

from flask import jsonify, request
from bs4 import BeautifulSoup

import requests

def comicextra_info():
    information = {
        'name': 'ComicExtra',
        'url': 'https://www.comicextra.com',
        'type': 'stream',
        'logo': 'https://www.comicextra.com/images/site/front/logo.png',
        'items': []
    }

    url = "https://www.comicextra.com/popular-comic"

    comicextra = requests.get(url)
    if comicextra.status_code == requests.codes.ok:
        comicextra_parser = BeautifulSoup(comicextra.text, 'html.parser')

        items = comicextra_parser.find_all('div', attrs={'class': 'cartoon-box'})
        for i in items:
            _id = i.a['href'].split('/')[-1]
            itm = {
                "name": i.find('h3').text,
                "cover": i.find('img')['src'],
                "detail": "/comics/comicextra/d/" + _id,
                "id": _id
            }
            information['items'].append(itm)

    return jsonify(information)

def comicextra_search(query):
    url = "https://www.comicextra.com/comic-search?key=" + query

    args = request.args
    if args.get('page'):
        url = "https://www.comicextra.com/comic-search?key=" + query + "&page=" + args.get('page')

    comicextra = requests.get(url)
    if comicextra.status_code == requests.codes.ok:
        comicextra_parser = BeautifulSoup(comicextra.text, 'html.parser')
        results = comicextra_parser.find_all('div', attrs={'class': 'cartoon-box'})
        resp = []
        for r in results:
            _id = r.a['href'].split('/')[-1]
            data = {
                "name": r.find('h3').a.text,
                "cover": r.find('img')['src'],
                "detail": "/comics/comicextra/d/" + _id,
                "id": _id
            }
            resp.append(data)
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to ComicExtra'}), 400

def comicextra_detail(comicid):
    url = "https://www.comicextra.com/comic/" + comicid

    comicextra = requests.get(url)
    if comicextra.status_code == requests.codes.ok:
        comicextra_parser = BeautifulSoup(comicextra.text, 'html.parser')

        resp = {
            "name": comicextra_parser.find('span', attrs={'class': 'title-1'}).text,
            "cover": comicextra_parser.find('div', attrs={'class': 'movie-image'}).find('img')['src'],
            "summary": comicextra_parser.find('div', attrs={'id': 'film-content'}).text.strip(),
            "status": comicextra_parser.find('dd', attrs={'class': 'status'}).a.text,
            "id": comicid,
            "genres": [],
            "chapters": []
        }

        detail_div = comicextra_parser.find('dl', attrs={'class': 'movie-dl'})
        genre_dd = detail_div.find_all('dd', attrs={'class': 'movie-dd'})[-1]
        genres = genre_dd.find_all('a')
        for g in genres:
            resp['genres'].append(g.text)

        chapters_div = comicextra_parser.find('tbody', attrs={'id': 'list'})
        chapters = chapters_div.find_all('tr')
        chapters.reverse()
        number = 1
        for c in chapters:
            chapter = {
                "name": c.td.a.text,
                "number": number,
                "detail": "/comics/comicextra/d/" + comicid + "/" + str(number)
            }
            resp['chapters'].append(chapter)
            number = number + 1
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to ComicExtra'}), 400

def comicextra_chapter(comicid, number):
    url = "https://www.comicextra.com/comic/" + comicid

    comicextra = requests.get(url)
    if comicextra.status_code == requests.codes.ok:
        comicextra_parser = BeautifulSoup(comicextra.text, 'html.parser')

        chapters_div = comicextra_parser.find('tbody', attrs={'id': 'list'})
        chapters = chapters_div.find_all('tr')
        chapters.reverse()

        chapter_url = chapters[number - 1].td.a['href'] + "/full"
        chapter_name = chapters[number - 1].td.a.text

        resp = {
            "name": chapter_name,
            "parent": "/comics/comicextra/d/" + comicid,
            "images": []
        }

        chapter = requests.get(chapter_url)
        if chapter.status_code == requests.codes.ok:
            chapter_parser = BeautifulSoup(chapter.text, 'html.parser')
            pages = chapter_parser.find_all('img', attrs={'class': 'chapter_img'})
            for p in pages:
                resp['images'].append(p['src'])

        return jsonify(resp)
    else:
        return jsonify({'error': 'Cannot connect to ComicExtra'})