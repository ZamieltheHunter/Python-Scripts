class NPC(dict):
    def __init__(self, name, data):
        dict.__init__(self)
        self['name'] = name
        self['gender'] = data['gender'] if 'gender' in data else "N"
        self['species'] = data['species'] if 'species' in data else "Undefined"
        self['text'] = data['text'] if 'text' in data else ""
        self['size'] = data['size'] if 'size' in data else "M (5 x 5)"
        self['speed'] = data['speed'] if 'speed' in data else 30
        self['experience'] = data['experience'] if 'experience' in data else 0
        self['traits'] = data['traits'] if 'traits' in data else {
            'initiative' : int(data['initiative']) if 'initiative' in data else 1,
            'defense' : int(data['defense']) if 'defense' in data else 1,
            'attack' : int(data['attack']) if 'attack' in data else 1,
            'resilience' : int(data['resilience']) if 'resilience' in data else 1,
            'competence' : int(data['competence']) if 'competence' in data else 1,
            'health' : int(data['health']) if 'health' in data else 1,
        }
        self['attributes'] = data['attributes'] if 'attributes' in data else {
            'str' : int(data['str']) if 'str' in data else 10,
            'dex' : int(data['dex']) if 'dex' in data else 10,
            'con' : int(data['con']) if 'con' in data else 10,
            'int' : int(data['int']) if 'int' in data else 10,
            'wis' : int(data['wis']) if 'wis' in data else 10,
            'cha' : int(data['cha']) if 'cha' in data else 10,
        }
