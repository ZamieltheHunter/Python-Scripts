class NPC(dict):
    def __init__(self, name, data):
        dict.__init__(self)
        self['name'] = name
        self['gender'] = data['gender'] if 'gender' in data else "N"
        self['species'] = data['species'] if 'species' in data else "Undefined"
        self['text'] = data['text'] if 'text' in data else ""
        self['traits'] = data['traits'] if 'traits' in data else {
            'initiative' : int(data['initiative']) if 'initiative' in data else 1,
            'defense' : int(data['defense']) if 'defense' in data else 1,
            'attack' : int(data['attack']) if 'attack' in data else 1,
            'resilience' : int(data['resilience']) if 'resilience' in data else 1,
            'competence' : int(data['competence']) if 'competence' in data else 1,
            'health' : int(data['health']) if 'health' in data else 1,
        }
