import json

intents = json.loads(open('intents.json').read())
for intent in intents['intents']:
    print(intent['patterns'])