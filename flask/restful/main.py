from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-very-long-super-secret-key'

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
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/myapp/api/v1/items', methods=['GET'])
def get_items():
    return jsonify({'items': ITEMS})

@app.route('/myapp/api/v1/items/id/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    item = [item for item in ITEMS if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})

@app.route('/myapp/api/v1/items/name/<string:item_name>', methods=['GET'])
def get_item_by_name(item_name):
    item = [item for item in ITEMS if item['name'] == item_name]
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})

@app.route('/myapp/api/v1/items', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        abort(404)
    item = {
        'id': ITEMS[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', "")
    }
    ITEMS.append(item)
    return jsonify({'item': item}), 201

@app.route('/myapp/api/v1/items/id/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = [item for item in ITEMS if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(404)
    item[0]['name'] = request.json.get('name', item[0]['name'])
    item[0]['description'] = request.json.get('description', item[0]['description'])
    return jsonify({'item': item})

@app.route('/myapp/api/v1/items/id/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = [item for item in ITEMS if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    ITEMS.remove(item[0])
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
