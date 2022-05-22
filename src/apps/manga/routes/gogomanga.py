"""
/gogomanga/s/<query>
{
    "name": "NAME",
    "cover": "COVER",
    "detail": "/gogomanga/d/ID",
    "id": ID
}
/gogomanga/d/<id>
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
            "detail": "/gogomanga/d/ID/NUMBER"
        }
    ]
}
/gogomanga/d/<id>/<number>
{
    "name": "NAME",
    "parent": "/gogomanga/d/ID",
    "images": []
}
"""

from flask import jsonify, request
from bs4 import BeautifulSoup

import requests

def gogomanga_search(query):
    url = "https://gogomanga.fun/?s=" + query

    args = request.args
    if args.get('page'):
        url = "https://gogomanga.fun/page/" + args.get('page') + "/?s=" + query
    
    gogomanga = requests.get(url)
    if gogomanga.status_code == requests.codes.ok:
        gogomanga_parser = BeautifulSoup(gogomanga.text, 'html.parser')
        results = gogomanga_parser.find_all('div', attrs={'class': 'bsx'})
        resp = []
        for r in results:
            _id = r.find('a')['href'].split('/')[-2]
            data = {
                "name": r.find('div', attrs={'class': 'tt'}).text.strip(),
                "cover": r.find('img')['src'],
                "detail": "/manga/gogomanga/d/" + _id,
                "id": _id
            }
            resp.append(data)
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to GogoManga'}), 400

def gogomanga_detail(mangaid):
    url = "https://gogomanga.fun/manga/" + mangaid

    gogomanga = requests.get(url)
    if gogomanga.status_code == requests.codes.ok:
        gogomanga_parser = BeautifulSoup(gogomanga.text, 'html.parser')

        resp = {
            "name": gogomanga_parser.find('h1', attrs={'class': 'entry-title'}).text,
            "cover": gogomanga_parser.find('img', class_="attachment- size- wp-post-image")['src'],
            "summary": "",
            "status": gogomanga_parser.find('div', class_="tsinfo").find('div').contents[-1].text,
            "id": mangaid,
            "genres": [],
            "chapters": []
        }

        genres_div = gogomanga_parser.find('span', attrs={'class': 'mgen'})
        genres = genres_div.find_all('a')
        for g in genres:
            resp['genres'].append(g.text)

        chapters = gogomanga_parser.find_all('div', attrs={'class': 'eph-num'})
        chapters.reverse()
        number = 1
        for c in chapters:
            chapter = {
                "name": c.find('span', attrs={'class': 'chapternum'}).text,
                "number": number,
                "detail": "/manga/gogomanga/d/" + str(mangaid) + "/" + str(number)
            }
            resp['chapters'].append(chapter)
            number = number + 1
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to GogoManga'}), 400

def gogomanga_chapter(mangaid, number):
    url = "https://gogomanga.fun/manga/" + mangaid

    gogomanga = requests.get(url)
    if gogomanga.status_code == requests.codes.ok:
        gogomanga_parser = BeautifulSoup(gogomanga.text, 'html.parser')

        chapters = gogomanga_parser.find_all('div', attrs={'class': 'eph-num'})
        chapters.reverse()

        chapter_url = chapters[number - 1].a['href']
        chapter_name = chapters[number - 1].find('span', attrs={'class': 'chapternum'}).text
        
        resp = {
            "name": chapter_name,
            "parent": "/manga/gogomanga/d/" + str(mangaid),
            "images": []
        }

        chapter = requests.get(chapter_url)
        if chapter.status_code == requests.codes.ok:
            chapter_parser = BeautifulSoup(chapter.text, 'html.parser')
            pages = chapter_parser.find_all('img', attrs={'class': 'size-full'})
            for p in pages:
                resp['images'].append(p['src'])
        
        return jsonify(resp)
    else:
        return jsonify({'error': 'Cannot connect to GogoManga'})