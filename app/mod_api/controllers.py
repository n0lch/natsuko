from app import app
##  If we get multiple database backends this is where they will get
##  conditionally imported.
import db_mongo as db
from flask import Response
try:
    import ujson as json
except ImportError:
    import json
import re

from flask import Blueprint
blueprint = Blueprint('api', __name__, subdomain=app.config['API_SUBDOMAIN'],
                        url_prefix=app.config['API_PREFIX'])

##  Implementing API for Natsuko Project, as specified in
##  https://w.n0l.ch/projects/natsuko/wiki/API
##  Note that tags & flags are really stubs for now.

##  TODO: learn Werkzeug routers to do regex matching in one pass

tt = '<regex("(~.*|/.+|;.+)?"):tail>'
tp = re.compile('(?P<tail>~'
                    '('
                        '(?P<last>[0-9]+)'
                        '(,'
                            '(?P<start>[0-9]+)'
                        ')?'
                    ')?'
                ')?'
                '(?P<tags>/[a-zA-Z0-9,]+)?'         # FIXME:
                '(?P<flags>;[a-zA-Z0-9,=]+)?')      #        these are stubs

def api_parser(tail):
    """Parses request url."""
    res = {}
    t = tp.fullmatch(tail)
    res['tail'] = t.group('tail') is not None
    res['last'] = t.group('last')
    res['start'] = t.group('start')
    res['tags'] = None if t.group('tags') is None else t.group('tags').split(',')
    res['flags'] = None if t.group('flags') is None else t.group('flags').split(',')
    return res

##  TODO: board/thread existance checking should be done even before
##        any regex matching and without database access, through some
##        sort of caching.
@blueprint.route('/<board>/' + tt)
def threads(board, tail):
    req = api_parser(tail)
    # /board/~ returns default number of threads
    if req.pop('tail') and not req['last']:
        req['last'] = app.config['API_LAST_THREADS']

    return Response(json.dumps(db.get_threads(board=board, **req)))

@blueprint.route('/<board>/<int:thread>' + tt)
def posts(board, thread, tail):
    req = api_parser(tail)
    # /board/1234~ returns default number of posts
    if req.pop('tail') and not req['last']:
        req['last'] = app.config['API_LAST_POSTS']

    return Response(json.dumps(
        db.get_posts(board=board, thread=thread, **req)))
