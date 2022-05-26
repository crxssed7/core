"""
/comicastle/s/<query>
{
    "name": "NAME",
    "cover": "COVER",
    "detail": "/comics/comicastle/d/ID",
    "id": ID
}
/comicastle/d/<id>
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
            "detail": "/comics/comicastle/d/ID/NUMBER"
        }
    ]
}
/comicastle/d/<id>/<number>
{
    "name": "NAME",
    "parent": "/comics/comicastle/d/ID",
    "images": []
}
"""

from flask import jsonify, request
from bs4 import BeautifulSoup

import requests

def comicastle_info():
    information = {
        'name': 'Comicastle',
        'url': 'https://comicastle.org',
        'type': 'stream',
        'items': []
    }

    url = "https://comicastle.org/library/postdate/desc"

    comicastle = requests.get(url)
    if comicastle.status_code == requests.codes.ok:
        comicastle_parser = BeautifulSoup(comicastle.text, 'html.parser')

        items = comicastle_parser.find_all('div', class_="col-xl-2 col-lg-3 col-md-3 col-6 mb-1 shadow-sm rounded")
        for i in items:
            _id = i.a['href'].split('/')[-2]
            itm = {
                "name": i.find('p', class_="font-small-3 mb-0 text-center text-bold-700").text.strip(),
                "cover": i.find('img')['data-src'],
                "detail": "/comics/comicastle/d/" + _id,
                "id": _id
            }
            information['items'].append(itm)

    return jsonify(information)

def comicastle_search(query):
    url = "https://comicastle.org/library/search/result"

    args = request.args
    if args.get('page'):
        url = "https://comicastle.org/library/search/result/" + args.get('page')

    body = {
        "search": query,
        "submit": "Submit"
    }

    comicastle = requests.post(url, data=body)
    if comicastle.status_code == requests.codes.ok:
        comicastle_parser = BeautifulSoup(comicastle.text, 'html.parser')
        results = comicastle_parser.find_all('div', class_='col-xl-2 col-lg-3 col-md-3 col-6 mb-2 shadow-sm rounded')
        resp = []
        for r in results:
            _id = r.a['href'].split('/')[-2]
            data = {
                "name": r.find('p', class_="font-small-3 mb-0 text-center text-bold-700").text,
                "cover": r.find('img')['data-src'],
                "detail": "/comics/comicastle/d/" + _id,
                "id": _id
            }
            resp.append(data)
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to Comicastle'}), 400

def comicastle_detail(comicid):
    url = "https://comicastle.org/home/detail/" + comicid

    comicastle = requests.get(url)
    if comicastle.status_code == requests.codes.ok:
        comicastle_parser = BeautifulSoup(comicastle.text, 'html.parser')

        detail_div = comicastle_parser.find('div', class_="col-12 col-md-7")

        resp = {
            "name": detail_div.h1.text,
            "cover": comicastle_parser.find('div', class_="d-flex align-items-center justify-content-center mb-1").img['data-src'],
            "summary": detail_div.find('p', attrs={'id': 'comic-desc'}).text,
            "status": detail_div.find('p', class_="font-small-3 text-bold-600").span.strong.text,
            "id": comicid,
            "genres": [],
            "chapters": []
        }

        genre_div = detail_div.find_all('div', class_="d-flex flex-row align-items-baseline")[-1]
        genres = genre_div.find_all('div', attrs={'style': 'padding:2px'})
        for g in genres:
            resp['genres'].append(g.button.text)
        
        chapters_table = comicastle_parser.find_all('table')[-1].tbody
        chapters = chapters_table.find_all('tr')
        number = 1
        for c in chapters:
            chapter = {
                "name": c.td.a.text.strip(),
                "number": number,
                "detail": "/comics/comicastle/d/" + comicid + "/" + str(number)
            }
            resp['chapters'].append(chapter)
            number = number + 1
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to Comicastle'}), 400

def comicastle_chapter(comicid, number):
    url = "https://comicastle.org/home/detail/" + comicid

    comicastle = requests.get(url)
    if comicastle.status_code == requests.codes.ok:
        comicastle_parser = BeautifulSoup(comicastle.text, 'html.parser')

        chapters_table = comicastle_parser.find_all('table')[-1].tbody
        chapters = chapters_table.find_all('tr')

        chapter_url = chapters[number - 1].td.a['href'].replace('pbp', 'swiper')
        chapter_name = chapters[number - 1].td.a.text.strip()

        resp = {
            "name": chapter_name,
            "parent": "/comics/comicastle/d/" + comicid,
            "images": []
        }

        chapter = requests.get(chapter_url)
        if chapter.status_code == requests.codes.ok:
            chapter_parser = BeautifulSoup(chapter.text, 'html.parser')
            pages = chapter_parser.find_all('div', attrs={'class': 'swiper-slide'})
            for p in pages:
                resp['images'].append(p.img['src'].strip())

        return jsonify(resp)
    else:
        return jsonify({'error': 'Cannot connect to ComicExtra'})