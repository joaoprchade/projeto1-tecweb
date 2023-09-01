import json
from database import Database, Note
from dataclasses import dataclass
import sqlite3


def extract_route(string):
    list = string.split(" ")
    list1 = list[1][1:]
    return list1


def read_file(path):
    with open(path, 'r+b') as f:
        return f.read()


def load_data(file):
    with open(f'data/{file}', 'r') as f:
        return json.loads(f.read())


def load_template(file):
    with open(f'templates/{file}', 'r') as f:
        return f.read()


def append_json(anotacao):
    with open('data/notes.json', 'r+') as f:
        file_data = json.load(f)
        file_data.append(anotacao)
        f.seek(0)
        json.dump(file_data, f, indent=4)


def build_response(body='', code=200, reason='OK', headers=''):
    final = f'HTTP/1.1 {code} {reason}'

    if headers:
        final += "\n" + headers

    final += "\n\n"+body
    return final.encode()
