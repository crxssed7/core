"""
{
    'name': 'NAME',
    'size': 'SIZE',
    'date': 'DATE',
    'seeders': SEEDERS,
    'leechers': LEECHERS,
    'link': 'LINK',
    'torrent': 'TORRENT',
    'magnet': 'MAGNET'
}
"""

from flask import jsonify, request
from bs4 import BeautifulSoup

import feedparser
import urllib.parse

def nyaa_info():
    information = {
        'name': 'Nyaa.si',
        'url': 'https://nyaa.si',
        'type': 'download'
    }
    return jsonify(information)

def nyaa(query, category=None):
    NYAA_CATEGORIES = {
        'anime': '1_0',
        'audio': '2_0',
        'literature': '3_0',
        'live': '4_0',
        'pictures': '5_0',
        'software': '6_0',
    }
    args = request.args
    url = 'https://nyaa.si/?page=rss&q=' + query
    # Figure out the category
    if args.get('category'):
        c = args.get('category')
        c_id = NYAA_CATEGORIES.get(c.lower())
        if c_id:
            url += '&c=' + c_id

    feed = feedparser.parse(url)
    resp = []
    for entry in feed.entries:
        data = {
            'name': entry.title,
            'size': entry.nyaa_size,
            'date': entry.published,
            'seeders': entry.nyaa_seeders,
            'leechers': entry.nyaa_leechers,
            'category': entry.nyaa_category,
            'link': entry.id,
            'torrent': entry.link,
            'magnet': 'magnet:?xt=urn:btih:' + entry.nyaa_infohash + '&dn=' + urllib.parse.quote(entry.title, safe='') + '&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce'
        }
        resp.append(data)
    return jsonify(resp)