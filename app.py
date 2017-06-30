#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

entries = [
    {
        'id':1,
        'text': 'Act I',
        'order': 1
    },
    {
        'id':2,
        'text': 'Act II',
        'order': 2
    }
]

@app.route('/chalk/api/1.0/entries', methods=['GET'])
#curl -i http://localhost:5000/chalk/api/1.0/entries
def get_entries():
    return jsonify({'entries': entries})

@app.route('/chalk/api/1.0/entry/<int:id>', methods=['GET'])
#curl -i http://localhost:5000/chalk/api/1.0/entries/1
def get_entry(id):
    entry = [entry for entry in entries if entry['id'] == id]
    if len(entry) == 0:
        abort(404)
    return jsonify({'entry': entry[0]})

@app.route('/chalk/api/1.0/entries', methods=['POST'])
#curl -i -H "Content-Type: application/json" -X POST -d
#'{"text": "Act III test"}' http://localhost:5000/chalk/api/1.0/entries
def create_entry():
    if not request.json:
        abort(400)
    entry = {
        'id': entries[-1]['id'] + 1,
        'text': request.json['text'],
        'order': max(entry['order'] for entry in entries)
    }
    entries.append(entry)
    return jsonify({'entry': entry}), 201

@app.route('/chalk/api/1.0/entries/<int:id>', methods=['PUT'])
#curl -i -H "Content-Type: application/json" -X PUT -d
#'{"text": "Act III test"}' http://localhost:5000/chalk/api/1.0/entries/2
def update_entry(id):
    entry = [entry for entry in entries if entry['id'] == id]
    if len(entry) == 0:
        abort(404)
    if not request.json:
        abort(400)
    #if 'text' in request.json and  type(request.json['text']) != 'unicode':
    #    abort(400)
    entry[0]['text'] = request.json.get('text', entry[0]['text'])
    return jsonify({'entry': entry[0]})

@app.route('/chalk/api/1.0/entries/<int:id>', methods=['DELETE'])
#curl -X DELETE http://localhost:5000/chalk/api/1.0/entries/2
def delete_entry(id):
    entry = [entry for entry in entries if entry['id'] == id]
    if len(entry) == 0:
        abort(404)
    entries.remove(entry[0])
    return jsonify({'Result': True})

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
