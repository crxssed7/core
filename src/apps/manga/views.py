from flask import Blueprint
from . import mangapill

manga = Blueprint('manga', __name__)

manga.add_url_rule('/mangapill/s/<query>', 'mangapill_search', mangapill.mangapill_search)
manga.add_url_rule('/mangapill/d/<int:mangaid>', 'mangapill_detail', mangapill.mangapill_detail)
manga.add_url_rule('/mangapill/d/<int:mangaid>/<int:number>', 'mangapill_chapter', mangapill.mangapill_chapter)