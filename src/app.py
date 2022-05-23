from flask import Flask, jsonify
from apps.torrents.views import torrents
from apps.comics.views import comics
from apps.manga.views import manga
from sources import SOURCES

def sources():
    return jsonify(SOURCES)

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(torrents, url_prefix="/torrents")
    app.register_blueprint(comics, url_prefix="/comics")
    app.register_blueprint(manga, url_prefix="/manga")
    
    app.add_url_rule('/sources/', 'sources', sources)

    return app

if __name__ == "__main__":
    create_app().run()