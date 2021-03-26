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

def str_th_len(text):
    length = 0
    for c in text:
        value = ord(c)
        if (value >= 3585 and value <= 3635 and value != 3633) or (value >= 3647 and value <= 3654) or (value >= 3663 and value <= 3675) or value == 144:
            length = length + 1
    return(length)

@app.route('/')
def home():
    if check_api_key():
        return jsonify({"message": "OK: Authorized"}), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

@app.route('/tokenize')
def tokenize():
    longstr = request.args.get('text', default = "", type = str)
    words_per_line = request.args.get('words_per_line', default = 0, type = int) # max 100
    keep_whitespace = request.args.get('whitespace', default = True)
    words_per_firstline = request.args.get('firstline', default = 0, type = int)
    if not check_api_key():
        return jsonify({"message": "ERROR: Unauthorized"}), 401
    if longstr != "":
        tokenized_words = word_tokenize(longstr, keep_whitespace=keep_whitespace)
        if words_per_line == 0:
            return jsonify({'tokenized': tokenized_words}), 200
        else:
            lines = []
            is_firstline = True
            wpl = words_per_line
            if is_firstline and words_per_firstline > 0:
                wpl = words_per_firstline

            words_added_this_line = 0
            line = ''
            count = 0
            for word in tokenized_words:
                if words_added_this_line <= wpl:
                    line = line + word
                    words_added_this_line = words_added_this_line + 1
                    
                    if count == len(tokenized_words) - 1:
                        lines.append(line)
                else:
                    is_firstline = False
                    wpl = words_per_line
                    lines.append(line)
                    
                    line = word
                    words_added_this_line = 1
                    if count == len(tokenized_words) - 1:
                        lines.append(line)
                count = count + 1
#            for line_number in range(0, math.ceil(len(tokenized_words)/words_per_line)):
#                line = ''
#                words_per_line_threshold = words_per_line
#                if is_firstline and words_per_firstline > 0:
#                    words_per_line_threshold = words_per_firstline
#
#                for i in range(0, words_per_line_threshold):
#                    if words_per_firstline > 0:
#                        word_index = line_number*words_per_line+i #TODO
#                    else:
#                        word_index = line_number*words_per_line+i
#                    if word_index >= len(tokenized_words):
#                        break
#                    line = line + tokenized_words[word_index]
#                is_firstline = False
#                lines.append(line)
            return jsonify({"tokenized": lines}), 200
    else:
        return jsonify({"message": "Invalid input"}), 200

@app.route('/tokenizeLen')
def tokenizeLen():
    longstr = request.args.get('text', default = "", type = str)
    char_per_line = request.args.get('char_per_line', default = 0, type = int)
    keep_whitespace = request.args.get('whitespace', default = True)
    char_per_firstline = request.args.get('firstline', default = 0, type = int)
    if not check_api_key():
        return jsonify({"message": "ERROR: Unauthorized"}), 401
    if longstr != "":
        tokenized_words = word_tokenize(longstr, keep_whitespace=keep_whitespace)
        if char_per_line == 0:
            return jsonify({'tokenized': tokenized_words}), 200
        else:
            lines = []
            line = ''
            count = 0

            is_firstline = True
            for word in tokenized_words:
                word_th_len = str_th_len(word)
                char_len_threshold = char_per_line
                if is_firstline and char_per_firstline > 0:
                    char_len_threshold = char_per_firstline

                if str_th_len(line) + word_th_len > char_len_threshold:
                    is_firstline = False
                    lines.append(line)
                    line = word
                else:
                    line = line + word
                if count == len(tokenized_words) - 1:
                    lines.append(line)
                count = count + 1
            return jsonify({"tokenized": lines}), 200
    else:
        return jsonify({"message": "Invalid input"}), 200


if __name__ == "__main__":
    app.run()

