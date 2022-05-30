"""
/mangafreak/s/<query>
{
    "name": "NAME",
    "cover": "COVER",
    "detail": "/mangafreak/d/ID",
    "id": ID
}
/mangafreak/d/<id>
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
            "detail": "/mangafreak/d/ID/NUMBER"
        }
    ]
}
/mangafreak/d/<id>/<number>
{
    "name": "NAME",
    "parent": "/mangafreak/d/ID",
    "images": []
}
"""

from flask import jsonify, request
from bs4 import BeautifulSoup

import requests

def mangafreak_info():
    information = {
        'name': 'Mangafreak',
        'url': 'https://w13.mangafreak.net',
        'type': 'stream',
        'logo': 'https://w13.mangafreak.net/misc/MF.ico',
        'items': []
    }

    url = "https://w13.mangafreak.net"

    mangafreak = requests.get(url)
    if mangafreak.status_code == requests.codes.ok:
        mangafreak_parser = BeautifulSoup(mangafreak.text, 'html.parser')

        items = mangafreak_parser.find_all('div', attrs={'class': 'latest_item'})
        for i in items:
            _id = i['datamanga']
            itm = {
                "name": i.find('a', attrs={'class': 'name'}).text,
                "cover": i.find('a', attrs={'class': 'image'}).img['src'],
                "id": _id,
                "detail": "/manga/mangafreak/d/" + _id
            }
            information['items'].append(itm)

    return jsonify(information)