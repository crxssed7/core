from flask import Blueprint
from .routes import getcomics
from .routes import comicextra

comics = Blueprint('comics', __name__)

comics.add_url_rule('/getcomics/', 'getcomics_info', getcomics.getcomics_info)
comics.add_url_rule('/getcomics/<query>/', 'getcomics', getcomics.getcomics)

comics.add_url_rule('/comicextra/', 'comicextra_info', comicextra.comicextra_info)
comics.add_url_rule('/comicextra/s/<query>/', 'comicextra_search', comicextra.comicextra_search)
comics.add_url_rule('/comicextra/d/<comicid>/', 'comicextra_detail', comicextra.comicextra_detail)
comics.add_url_rule('/comicextra/d/<comicid>/<int:number>/', 'comicextra_chapter', comicextra.comicextra_chapter)