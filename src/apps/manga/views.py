from flask import Blueprint, jsonify
from .routes import mangapill
from .routes import gogomanga

from sources import SOURCES

manga = Blueprint('manga', __name__)

@manga.route('/')
def src_manga():
    return jsonify(SOURCES['manga'])

manga.add_url_rule('/mangapill/', 'mangapill_info', mangapill.mangapill_info)
manga.add_url_rule('/mangapill/s/<query>/', 'mangapill_search', mangapill.mangapill_search)
manga.add_url_rule('/mangapill/d/<int:mangaid>/', 'mangapill_detail', mangapill.mangapill_detail)
manga.add_url_rule('/mangapill/d/<int:mangaid>/<int:number>/', 'mangapill_chapter', mangapill.mangapill_chapter)

manga.add_url_rule('/gogomanga/', 'gogomanga_info', gogomanga.gogomanga_info)
manga.add_url_rule('/gogomanga/s/<query>/', 'gogomanga_search', gogomanga.gogomanga_search)
manga.add_url_rule('/gogomanga/d/<mangaid>/', 'gogomanga_detail', gogomanga.gogomanga_detail)
manga.add_url_rule('/gogomanga/d/<mangaid>/<int:number>/', 'gogomanga_chapter', gogomanga.gogomanga_chapter)