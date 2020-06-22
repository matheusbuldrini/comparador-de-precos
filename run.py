from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_from_directory
import os
import json
from comparador import search_all_interleave

app = Flask(__name__)

app.secret_key = 'any random stringldshfaslicynonrycxuowehnmsda 35fg234dfcv43c4c'


@app.route("/")
def index():
    return render_template('index.html', ads=[])

@app.route("/search", methods=['GET'])
def search():
    s = request.args.get("q")
    ads = search_all_interleave(s)
    return render_template('index.html', ads=ads['ads'])





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=True)