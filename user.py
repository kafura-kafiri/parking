from flask import Blueprint, render_template, request
from config import users
from tools.utility import obj2str, request_json
from flask_login import login_required, current_user
from crud.views import user

messages = {
    'saved',
    'required',
    'segment',
    'invalid',
    'already',
    'character',
    '2num',
    'bad',

    'updated',
    'removed',
    'not_saved',
    'not_removed',
    'saved',
}

@user.blue.route('/me')
#@login_required
def get_profile():
    return render_template('user/profile.html')


@user.blue.route('/me$', methods=['GET', 'POST'])
#@login_required
def update_profile():
    from pymongo import ReturnDocument
    try:
        node = request.values['node']
        _json = request_json(request, specific_type=None)
        user = users.find_one_and_update(
            {'_id': current_user._id},
            {"$set": {node: _json}},
            return_document=ReturnDocument.AFTER
        )
        id = user.id
        current_user.__dict__ = user
        current_user.id = id
    except: pass
    return render_template('user/profile_plus.html')
