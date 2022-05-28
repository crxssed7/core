from flask import Blueprint
from .routes import tenshi

anime = Blueprint('anime', __name__)

anime.add_url_rule('/tenshi/s/<query>/', 'tenshi_search', tenshi.tenshi_search)
anime.add_url_rule('/tenshi/d/<animeid>/', 'tenshi_detail', tenshi.tenshi_detail)
anime.add_url_rule('/tenshi/d/<animeid>/<int:number>/', 'tenshi_episode', tenshi.tenshi_episode)