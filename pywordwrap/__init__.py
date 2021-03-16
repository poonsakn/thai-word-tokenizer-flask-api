from flask import Flask, request, jsonify
from pythainlp import word_tokenize
import sys
import math
import constants

app = Flask(__name__)

def check_api_key():
    headers = request.headers
    auth = headers.get("x-api-key")
    if auth == constants.apikey:
        return True
    else:
        return False

@app.route('/')
def home():
    if check_api_key():
        return jsonify({"message": "OK: Authorized"}), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

@app.route('/tokenize')
def tokenize():
    longstr = request.args.get('text', default = "", type = str)
    words_per_line = request.args.get('wpl', default = 0, type = int) # max 100
    keep_whitespace = request.args.get('whitespace', default = False)
    if not check_api_key():
        return jsonify({"message": "ERROR: Unauthorized"}), 401
    if longstr != "":
        tokenized_words = word_tokenize(longstr, keep_whitespace=keep_whitespace)
        if words_per_line == 0:
            return jsonify({'tokenized': tokenized_words}), 200
        else:
            lines = []
            for line_number in range(0, math.ceil(len(tokenized_words)/words_per_line)):
                line = ''
                for i in range(0, words_per_line):
                    word_index = line_number*words_per_line+i
                    if word_index >= len(tokenized_words):
                        break
                    line = line + tokenized_words[word_index]
                lines.append(line)
            return jsonify({"tokenized": lines}), 200
    else:
        return jsonify({"message": "Invalid input"}), 200


if __name__ == "__main__":
    app.run()

