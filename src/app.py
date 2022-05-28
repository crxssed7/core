from flask import Flask, jsonify
from apps.downloaders.views import downloaders
from apps.comics.views import comics
from apps.manga.views import manga
from apps.anime.views import anime
from sources import SOURCES

def sources():
    return jsonify(SOURCES)

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(downloaders, url_prefix="/downloads")
    app.register_blueprint(comics, url_prefix="/comics")
    app.register_blueprint(manga, url_prefix="/manga")
    app.register_blueprint(anime, url_prefix="/anime")
    
    app.add_url_rule('/sources/', 'sources', sources)

    return app

if __name__ == "__main__":
    create_app().run()