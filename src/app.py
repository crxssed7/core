from flask import Flask
from apps.torrents.views import torrents
from apps.comics.views import comics
from apps.manga.views import manga

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(torrents, url_prefix="/torrents")
    app.register_blueprint(comics, url_prefix="/comics")
    app.register_blueprint(manga, url_prefix="/manga")
    
    return app

if __name__ == "__main__":
    create_app().run()