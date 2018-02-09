"""Restful api example using standard flask and flask-limiter."""
from flask import Flask, jsonify, abort, make_response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-very-long-super-secret-key'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["30 per minute", "1 per second"],
)

ITEMS = [
    {'id': 1,
     'name': 'item1',
     'description': "some description for item1"},
    {'id': 2,
     'name': 'item2',
     'description': "some description for item2"}
]


# Avoid html response for errors
@app.errorhandler(404)
def not_found(error):
    """Return json response for not found."""
    return make_response(jsonify({'error': 'Not found'}), 404)


# Avoid html response for errors
@app.errorhandler(400)
def bad_request(error):
    """Return json response for bad request."""
    return make_response(jsonify({'error': 'Bad Request'}), 400)


# Avoid html response for errors - limiters
@app.errorhandler(429)
def too_many_request(error):
    """Return json response for bad request."""
    return make_response(jsonify({'error': 'Too Many Requests'}), 429)


@app.route('/myapp/api/v1/items', methods=['GET'])
def get_items():
    """Return all items."""
    return jsonify({'items': ITEMS})


@app.route('/myapp/api/v1/items/id/<int:item_id>', methods=['GET'])
@limiter.limit("5 per minute")
def get_item_by_id(item_id):
    """Return item by ID."""
    item = [item for item in ITEMS if item['id'] == item_id]
    if not item:
        abort(404)
    return jsonify({'item': item[0]})


@app.route('/myapp/api/v1/items/name/<string:item_name>', methods=['GET'])
@limiter.exempt
def get_item_by_name(item_name):
    """Return item by name."""
    item = [item for item in ITEMS if item['name'] == item_name]
    if not item:
        abort(404)
    return jsonify({'item': item[0]})


@app.route('/myapp/api/v1/items', methods=['POST'])
@limiter.limit("15 per minute")
def create_item():
    """Create new item."""
    if not request.json or 'name' not in request.json:
        abort(400)
    item = {
        'id': ITEMS[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', "")
    }
    ITEMS.append(item)
    return jsonify({'item': item}), 201


@app.route('/myapp/api/v1/items/id/<int:item_id>', methods=['PUT'])
@limiter.limit("5 per minute")
def update_item(item_id):
    """Update item by ID."""
    item = [item for item in ITEMS if item['id'] == item_id]
    if not item:
        abort(404)
    if not request.json:
        abort(404)
    item[0]['name'] = request.json.get('name', item[0]['name'])
    item[0]['description'] = request.json.get('description',
                                              item[0]['description'])
    return jsonify({'item': item})


@app.route('/myapp/api/v1/items/id/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item from items by ID."""
    item = [item for item in ITEMS if item['id'] == item_id]
    if not item:
        abort(404)
    ITEMS.remove(item[0])
    return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)
