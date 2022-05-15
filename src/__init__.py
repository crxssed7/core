from flask import Flask, jsonify
from routes import nyaa, eztv

app = Flask(__name__)

app.add_url_rule('/nyaa/<query>', 'nyaa', nyaa)
app.add_url_rule('/eztv/<query>', 'eztv', eztv)

if __name__ == '__main__':
    app.run()