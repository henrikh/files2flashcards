import json
import urllib.request

deck_name = "Default"

def invoke(action, params):
    payload = {'action': action, 'params': params, 'version': 6}

    request_json = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request('http://localhost:8765', request_json)
    response = json.load(urllib.request.urlopen(request))

    if response['error'] is not None:
        raise Exception(response['error'])

    return response['result']

def add_note(note_type, fields):
    params = {"note": {
        "deckName": deck_name,
        "modelName": note_type,
        "fields": fields,
        "options": {
            "allowDuplicates": False
            },
        "tags": []
        }}

    return invoke("addNote", params)

def update_note(note_id, fields):
    params = {"note":{
        "id": note_id,
        "fields": fields
        }}

    invoke("updateNoteFields", params)