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
from flask import jsonify, request, Blueprint
from bs4 import BeautifulSoup

import feedparser
import requests
import urllib.parse

torrents = Blueprint('torrents', __name__)

@torrents.route('/nyaa/<query>')
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

@torrents.route('/eztv/<query>')
def eztv(query):
    url = 'https://eztv.ro/search/' + query
    try:
        eztv = requests.get(url)
        if eztv.status_code == requests.codes.ok:
            doc_response = eztv.text
            eztv_parser = BeautifulSoup(doc_response, 'html.parser')
            results = eztv_parser.find_all('tr', attrs={'name': 'hover'})
            resp = []
            for r in results:
                torrent_link = ''
                try:
                    torrent_link = r.find_all('td')[2].find_all('a')[1]['href']
                except IndexError:
                    torrent_link = ''

                magnet_link = ''
                try:
                    magnet_link = r.find_all('td')[2].find_all('a')[0]['href']
                except IndexError:
                    magnet_link = ''
                
                data = {
                    'name': r.find('a', attrs={'class', 'epinfo'}).text.strip(),
                    'size': r.find_all('td')[3].text,
                    'date': r.find_all('td')[4].text,
                    'seeders': r.find_all('td')[5].text,
                    'leechers': '',
                    'category': '',
                    'link': 'https://eztv.ro' + r.find('a', attrs={'class', 'epinfo'})['href'],
                    'torrent': torrent_link,
                    'magnet': magnet_link
                }
                resp.append(data)
            return jsonify(resp)
        else:
            return jsonify({'error': 'Could not connect to EZTV'}), 400
    except BaseException as e:
        return jsonify({'error': str(e)}), 400