"""
{
    'name': 'NAME',
    'size': 'SIZE',
    'publisher': 'PUBLISHER',
    'date': 'DATE',
    'link': 'LINK',
    'downloads': [
        {
            'name': 'DOWNLOAD NAME',
            'link': 'LINK'
        }
    ]
}
"""
from flask import jsonify, request, Blueprint
from bs4 import BeautifulSoup

import requests

comics = Blueprint('comics', __name__)

@comics.route('/getcomics/<query>')
def getcomics(query):
    url = 'https://getcomics.info/?s=' + query

    args = request.args
    if args.get('page'):
        url = 'https://getcomics.info/page/' + args.get('page') + '/?s=' + query

    getcomics = requests.get(url)
    if getcomics.status_code == requests.codes.ok:
        doc_response = getcomics.text
        getcomics_parser = BeautifulSoup(doc_response, 'html.parser')
        results = getcomics_parser.find_all('article', attrs={'class': 'post'})
        resp = []
        for r in results:
            # Load the detail page
            detail = requests.get(r.find('h1', attrs={'class': 'post-title'}).a['href'])
            detail_parser = BeautifulSoup(detail.text, 'html.parser')
            date = detail_parser.find('time').text
            downloads = []
            dl_btns = detail_parser.find_all('div', attrs={'class': 'aio-button-center'})
            for dl in dl_btns:
                name = dl.a.contents[-1]
                link = dl.a['href']
                dls = {
                    'name': name,
                    'link': link
                }
                downloads.append(dls)

            data = {
                'name': r.find('h1', attrs={'class': 'post-title'}).a.text,
                'size': r.find('p', attrs={'style': 'text-align: center;'}).contents[3].strip(),
                'publisher': r.find('a', attrs={'class': 'post-category'}).text,
                'date': date,
                'link': r.find('h1', attrs={'class': 'post-title'}).a['href'],
                'downloads': downloads
            }
            resp.append(data)
        return jsonify(resp)
    else:
        return jsonify({'error': 'Could not connect to GetComics'}), 400