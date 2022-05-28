"""
/tenshi/s/<query>
{
    "name": "NAME",
    "cover": "COVER",
    "detail": "/anime/tenshi/d/ID",
    "id": ID
}
/tenshi/d/<id>
{
    "name": "NAME",
    "cover": "COVER",
    "summary": "SUMMARY",
    "status": "STATUS",
    "genres": []
    "id": ID,
    "episodes": [
        {
            "name": "NAME",
            "number": "NUMBER",
            "detail": "/anime/tenshi/d/ID/NUMBER"
        }
    ]
}
/tenshi/d/<id>/<number>
{
    "name": "NAME",
    "parent": "/anime/tenshi/d/ID",
    "videos": "VIDEO"
}
"""

from flask import jsonify, request
from bs4 import BeautifulSoup

import requests

def tenshi_search(query):
    url = "https://tenshi.moe/anime?q=" + query

    args = request.args
    if args.get('page'):
        url = "https://tenshi.moe/anime?q=" + query + "&page=" + args.get('page')

    s = requests.Session()
    s.cookies.set('loop-view', 'thumb', domain='tenshi.moe')

    tenshi = s.get(url)
    if tenshi.status_code == requests.codes.ok:
        tenshi_parser = BeautifulSoup(tenshi.text, 'html.parser')
        results_div = tenshi_parser.find('ul', class_='loop anime-loop thumb')
        results = results_div.find_all('li')
        resp = []
        for r in results:
            _id = r.a['href'].split('/')[-1]
            data = {
                "name": r.find('span', attrs={'class': 'thumb-title'}).text,
                "cover": r.find('img', attrs={'class': 'image'})['src'],
                "detail": "/anime/tenshi/d/" + _id,
                "id": _id
            }
            resp.append(data)
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to Tenshi'}), 400

def tenshi_detail(animeid):
    url = "https://tenshi.moe/anime/" + animeid

    tenshi = requests.get(url)
    if tenshi.status_code == requests.codes.ok:
        tenshi_parser = BeautifulSoup(tenshi.text, 'html.parser')

        resp = {
            "name": tenshi_parser.find('header', attrs={'class': 'entry-header'}).h1.text,
            "cover": tenshi_parser.find('img', attrs={'class': 'cover-image'})['src'],
            "summary": tenshi_parser.find('section', attrs={'class': 'entry-description'}).find('div', attrs={'class': 'card-body'}).text.strip(),
            "status": tenshi_parser.find('li', attrs={'class': 'status'}).find('span', attrs={'class': 'value'}).a.text.strip(),
            "genres": [],
            "id": animeid,
            "episodes": []
        }

        genres = tenshi_parser.find('li', attrs={'class': 'genre'}).find_all('span', attrs={'class': 'value'})
        for g in genres:
            resp['genres'].append(g.a.text)

        episodes = tenshi_parser.find('ul', attrs={'class': 'episode-loop'}).find_all('li')
        number = 1
        for e in episodes:
            episode = {
                "name": e.find('div', attrs={'class': 'episode-label'}).span.text,
                "number": number,
                "detail": "/anime/tenshi/d/" + animeid + "/" + str(number)
            }
            resp['episodes'].append(episode)
            number = number + 1
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to Tenshi'}), 400

def tenshi_episode(animeid, number):
    url = "https://tenshi.moe/anime/" + animeid

    tenshi = requests.get(url)
    if tenshi.status_code == requests.codes.ok:
        tenshi_parser = BeautifulSoup(tenshi.text, 'html.parser')

        episodes = tenshi_parser.find('ul', attrs={'class': 'episode-loop'}).find_all('li')

        episode_url = episodes[number - 1].a['href']
        episode_name = episodes[number - 1].find('div', attrs={'class': 'episode-label'}).span.text

        resp = {
            "name": episode_name,
            "parent": "/anime/tenshi/d/" + animeid,
            "video": ""
        }

        episode = requests.get(episode_url)
        if episode.status_code == requests.codes.ok:
            episode_parser = BeautifulSoup(episode.text, 'html.parser')
            
            print(episode_url)
            video = episode_parser.find('div', attrs={'class': 'plyr__video-wrapper'})

            resp['video'] = "video.text"

        return jsonify(resp)
    else:
        return jsonify({'error': 'Cannot connect to Tenshi'})