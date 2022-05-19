"""
/mangapill/s/<query>
{
    "name": "NAME",
    "cover": "COVER",
    "detail": "/mangapill/d/ID",
    "id": ID
}
/mangapill/d/<id>
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
            "detail": "/mangapill/d/ID/NUMBER"
        }
    ]
}
/mangapill/d/<id>/<number>
{
    "name": "NAME",
    "parent": "/mangapill/d/ID",
    "images": []
}
"""

from flask import jsonify, request
from bs4 import BeautifulSoup

import requests

def mangapill_search(query):
    url = "https://mangapill.com/search?q=" + str(query).replace(' ', '+')

    args = request.args
    if args.get('page'):
        url = "https://mangapill.com/search?q=" + str(query).replace(' ', '+') + "&page=" + args.get('page')

    mangapill = requests.get(url)
    if mangapill.status_code == requests.codes.ok:
        mangapill_parser = BeautifulSoup(mangapill.text, 'html.parser')
        results_div = mangapill_parser.find('div', class_="my-3 grid justify-end gap-3 grid-cols-2 md:grid-cols-3 lg:grid-cols-5")
        results = results_div.find_all('div', class_="")
        resp = []
        for r in results:
            _id = str(r.a['href']).split('/')[2]
            data = {
                "name": r.find('div', class_="mt-3 font-black leading-tight line-clamp-2").text,
                "cover": r.a.figure.img['data-src'],
                "id": _id,
                "detail": "/manga/mangapill/d/" + _id
            }
            resp.append(data)
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to MangaPill'}), 400

def mangapill_detail(mangaid):
    url = "https://mangapill.com/manga/" + str(mangaid)
    
    mangapill = requests.get(url)
    if mangapill.status_code == requests.codes.ok:
        mangapill_parser = BeautifulSoup(mangapill.text, 'html.parser')

        detail_div = mangapill_parser.find('div', class_="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3")

        resp = {
            "name": mangapill_parser.find('h1', class_="font-bold text-lg md:text-2xl").text,
            "cover": mangapill_parser.find('img')['data-src'],
            "summary": mangapill_parser.find('p', class_="text-sm text--secondary").text,
            "status": detail_div.find_all('div', class_="")[3].text,
            "id": mangaid,
            "genres": [],
            "chapters": []
        }

        genres = mangapill_parser.find_all('a', class_="text-sm mr-1 text-brand")
        for g in genres:
            resp['genres'].append(g.text)

        chapters_div = mangapill_parser.find('div', class_='my-3 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6')
        chapters = chapters_div.find_all('a')
        chapters.reverse()
        number = 1
        for c in chapters:
            chapter = {
                "name": c.text,
                "number": number,
                "detail": "/manga/mangapill/d/" + str(mangaid) + "/" + str(number)
            }
            resp['chapters'].append(chapter)
            number = number + 1
        return jsonify(resp)
    else:
        return jsonify({'error': 'Cannot connect to MangaPill'}), 400

def mangapill_chapter(mangaid, number):
    url = "https://mangapill.com/manga/" + str(mangaid)
    
    mangapill = requests.get(url)
    if mangapill.status_code == requests.codes.ok:
        mangapill_parser = BeautifulSoup(mangapill.text, 'html.parser')

        chapters_div = mangapill_parser.find('div', class_='my-3 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6')
        chapters = chapters_div.find_all('a')
        chapters.reverse()

        chapter_url = "https://mangapill.com" + chapters[number - 1]['href']
        chapter_name = chapters[number - 1].text

        resp = {
            "name": chapter_name,
            "parent": "/manga/mangapill/d/" + str(mangaid),
            "images": []
        }

        chapter = requests.get(chapter_url)
        if chapter.status_code == requests.codes.ok:
            chapter_parser = BeautifulSoup(chapter.text, 'html.parser')
            pages = chapter_parser.find_all('img', attrs={'class': 'js-page'})
            for p in pages:
                resp['images'].append(p['data-src'])
        
        return jsonify(resp)
    else:
        return jsonify({'error': 'Cannot connect to MangaPill'})