from flask import Flask

# blueprint import
from apps.torrents.views import torrents

def create_app():
    app = Flask(__name__)
    
    # register blueprint
    app.register_blueprint(torrents, url_prefix="/torrents")
    
    return app

if __name__ == "__main__":
    create_app().run()