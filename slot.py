from flask import Blueprint, request, jsonify, abort
from flask_login import current_user
from config import Slot as slots, Segment as segments, db
import json
blu = Blueprint('slot', '__name__', url_prefix='/slots')
import datetime
import jwt
import pyqrcode


@blu.route('/', methods=['POST'])
def insert_slot():
    code = request.form['code']
    slot = slots(code, 1)  # todo change to current user
    db.session.add(slot)
    db.session.commit()
    return json.dumps({'success': True, '_id': slot._id}), 200, {'ContentType': 'application/json'}


@blu.route('/<int:_id>', methods=['DELETE'])
def delete_slot(_id):
    slots.query.filter_by(_id=_id).delete()
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@blu.route('/<_id>', methods=['GET'])
def get_slot(_id):
    slot = slots.query.filter_by(_id=_id).first()
    return jsonify({
        'code': slot.code,
        '_date': slot._date,
        '_author': slot._author,
        '_id': slot._id,
    })


@blu.route('/<_id>/<int:head>,<int:tail>', methods=['GET', 'POST'])
def get_jwt(_id, head, tail):
    _json = {
        'head': head,
        'tail': tail,
        '_id': _id
    }
    return jwt.encode(_json, 'secret', algorithm='HS256').decode('utf-8')


@blu.route('/<_id>/', methods=['POST'])
def insert_segment(_id):
    payload = jwt.decode(request.form['jwt'], 'secret', algorithms=['HS256'])
    head = datetime.datetime.fromtimestamp(payload['head'])
    tail = datetime.datetime.fromtimestamp(payload['tail'])
    segment = segments(payload['_id'], head, tail, 1)  # todo  change to current user
    db.session.add(segment)
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@blu.route('/<int:_id>/grant', methods=['POST'])
def grant_segment(_id):
    now = datetime.datetime.now()
    _segments = segments.query.filter_by(slot=_id, ).filter(segments.head <= now).filter(now <= segments.tail)
    _segment = _segments[0]
    for segment in _segments:
        if segment.tail - segment.head < _segment.tail - _segment.head:
            _segment = segment
    if _segment.author == 1:  # todo change to current user
        qr = pyqrcode.create(str(_segment))
        return qr.terminal()
    abort(403)
#
# @blu.route('/')