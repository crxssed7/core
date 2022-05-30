from flask import Flask, jsonify, render_template
from apps.comics.views import comics
from apps.manga.views import manga
from sources import SOURCES

def sources():
    return jsonify(SOURCES)

def home():
    return render_template('index.html', comics=SOURCES['comics'], manga=SOURCES['manga'])

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(comics, url_prefix="/comics/")
    app.register_blueprint(manga, url_prefix="/manga")
    
    app.add_url_rule('/sources/', 'sources', sources)
    app.add_url_rule('/', 'home', home)

    return app

if __name__ == "__main__":
    create_app().run()