from flask import Blueprint
blu = Blueprint('slot', '__name__', url_prefix='/slots')

@blu.route('/', methods=['POST'])
@blu.route('/', methods=['DELETE'])
@blu.route('/<_id>', methods=['GET'])


@blu.route('/<_id>/<head>,<tail>', methods=['GET'])
@blu.route('/<_id>/', methods=['POST'])

@blu.route('/')