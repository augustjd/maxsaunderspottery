#!./env/bin/python

from sand import app
import os


def is_superuser():
    return os.geteuid() == 0

if __name__ == '__main__':
    port = 80 if is_superuser() else 8000

    for rule in app.url_map.iter_rules():
        print(rule)

    app.run('127.0.0.1', debug=True, port=port)
