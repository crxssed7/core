from flask import Blueprint
from .routes import nyaa
from .routes import eztv
from .routes import getcomics

downloaders = Blueprint('downloads', __name__)

downloaders.add_url_rule('/getcomics/', 'getcomics_info', getcomics.getcomics_info)
downloaders.add_url_rule('/getcomics/<query>/', 'getcomics', getcomics.getcomics)

downloaders.add_url_rule('/nyaa/', 'nyaa_info', nyaa.nyaa_info)
downloaders.add_url_rule('/nyaa/<query>/', 'nyaa', nyaa.nyaa)

downloaders.add_url_rule('/eztv/', 'eztv_info', eztv.eztv_info)
downloaders.add_url_rule('/eztv/<query>/', 'eztv', eztv.eztv)