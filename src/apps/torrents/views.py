from flask import Blueprint
from .routes import nyaa
from .routes import eztv

torrents = Blueprint('torrents', __name__)

torrents.add_url_rule('/nyaa/', 'nyaa_info', nyaa.nyaa_info)
torrents.add_url_rule('/nyaa/<query>/', 'nyaa', nyaa.nyaa)

torrents.add_url_rule('/eztv/', 'eztv_info', eztv.eztv_info)
torrents.add_url_rule('/eztv/<query>/', 'eztv', eztv.eztv)