from flask import Flask
import json

with open("Flask_server/config.json", "r") as data:
    config = json.load(data)

app = Flask(__name__)
app.config = dict(app.config, **config)
app.secret_key = config['key']

import Flask_server.routes
