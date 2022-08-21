import os
from typing import List
from time import time


BASE_PATH = '/recordings'
MAX_AGE = int(os.getenv('NVR_MAX_AGE', '60'))


def age(path):
    """Finds the newest file in the directory and returns its age."""
    max_age = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                max_age = max(max_age, entry.stat().st_mtime)
    return time() - max_age


def subfolders(path) -> List[os.DirEntry]:
    """Returns the subfolders in given path."""
    with os.scandir(path) as it:
        return [e for e in it if e.is_dir() and e.name != 'lost+found']


def app(environ, start_response):
    """Implements the WSGI protocol."""
    paths = subfolders(BASE_PATH)

    result = [(p.name, age(p)) for p in paths]
    stale = any(r[1] > MAX_AGE for r in result)
    text = '\n'.join(f'{r[0]}: {r[1]}' for r in result) + '\n' + ('Fresh' if not stale else 'Stale') + '\n'

    start_response('500 Internal Server Error' if stale else '200 OK', [('Content-Type', 'text/plain')])
    yield text.encode()
