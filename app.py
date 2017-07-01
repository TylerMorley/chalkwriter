#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

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

#curl -i http://localhost:5000/chalk/api/1.0/entries
@app.route('/chalk/api/1.0/entries', methods=['GET'])
def get_entries():
    return jsonify({'entries': [make_public_entry(entry) for entry in entries]})

#curl -i http://localhost:5000/chalk/api/1.0/entries/1
@app.route('/chalk/api/1.0/entries/<int:id>', methods=['GET'])
def get_entry(id):
    entry = [entry for entry in entries if entry['id'] == id]
    if len(entry) == 0:
        abort(404)
    return jsonify({'entry': make_public_entry(entry[0])})

#curl -i -H "Content-Type: application/json" -X POST -d
#'{"text": "Act III test"}' http://localhost:5000/chalk/api/1.0/entries
@app.route('/chalk/api/1.0/entries', methods=['POST'])
def create_entry():
    if not request.json:
        abort(400)
    entry = {
        'id': entries[-1]['id'] + 1,
        'text': request.json['text'],
        'order': max(entry['order'] for entry in entries)
    }
    entries.append(entry)
    return jsonify({'entry': make_public_entry(entry)}), 201

#curl -i -H "Content-Type: application/json" -X PUT -d
#'{"text": "Act II the imposter"}' http://localhost:5000/chalk/api/1.0/entries/2
@app.route('/chalk/api/1.0/entries/<int:id>', methods=['PUT'])
def update_entry(id):
    entry = [entry for entry in entries if entry['id'] == id]
    if len(entry) == 0:
        abort(404)
    if not request.json:
        abort(400)
    #if 'text' in request.json and  type(request.json['text']) != 'unicode':
    #    abort(400)
    entry[0]['text'] = request.json.get('text', entry[0]['text'])
    return jsonify({'entry': make_public_entry(entry[0])})

#curl -X DELETE http://localhost:5000/chalk/api/1.0/entries/2
@app.route('/chalk/api/1.0/entries/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_entry(id):
    entry = [entry for entry in entries if entry['id'] == id]
    if len(entry) == 0:
        abort(404)
    entries.remove(entry[0])
    return jsonify({'Result': True})

def make_public_entry(entry):
    new_entry = {}
    for field in entry:
        if field == 'id':
            new_entry['uri'] = url_for(
                'get_entry',
                id=entry['id'],
                _external=True
            )
        else:
            new_entry[field] = entry[field]
    return new_entry

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.get_password
def get_password(username):
    if username == 'Miguel':
        return 'MyPassword'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error":"Unauthorized access"}), 401)

if __name__ == '__main__':
    app.run(debug=True)
