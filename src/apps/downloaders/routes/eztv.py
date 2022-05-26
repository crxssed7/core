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

import requests

def eztv_info():
    information = {
        'name': 'Eztv',
        'url': 'https://eztv.ro',
        'type': 'download'
    }
    return jsonify(information)

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