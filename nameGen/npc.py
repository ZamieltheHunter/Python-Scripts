class NPC(dict):

    def __init__(self, name, data):
        dict.__init__(self)
        speciesDict = {
            "Drake" : {
                "type" : "Beast",
                "size" : "L(2x3)",
                "reach" : 2,
                "speed" : 30,
                "qualities": [],
            },
            "Dwarf" : {
                "speed" : 20,
                "qualities": []
            },
            "Elf" : {
                "type" : "Fey",
                "qualities": []
            },
            "Giant" : {
                "size" : "L(2x2)",
                "reach" : 2,
                "speed" : 50,
                "qualities": []
            },
            "Goblin" : {
                "size" : "S(1x1)",
                "speed" : 20,
                "qualities": []
            },
            "Ogre" : {
                "size" : "L(2x2)",
                "qualities" : []
            },
            "Orc" : {
                "qualities" : []
            },
            "Pech" : {
                "size" : "S(1x1)",
                "qualities" : []
            },
            "Rootwalker" : {
                "type" : "Plant",
                "size" : "L(2x2)",
                "qualities" : []
            },
            "Saurian" : {
                "qualities" : []
            },
            "Unborn" : {
                "type" : "Construct",
                "speed" : 20,
                "qualities" : []
            }
        }
        self['name'] = name
        self['gender'] = data['gender'] if 'gender' in data else "N"
        self['species'] = data['species'] if 'species' in data else "Other"
        self['text'] = data['text'] if 'text' in data else ""
        self['size'] = data['size'] if 'size' in data else "M(1x1)"
        self['speed'] = data['speed'] if 'speed' in data else 30
        self['experience'] = data['experience'] if 'experience' in data else 0
        self['type'] = data['type'] if 'type' in data else 'Folk'
        self['reach'] = data['reach'] if 'reach' in data else 1
        self['attackList'] = data['attackList'] if 'attackList' in data else {}
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
        
        if self['species'] in speciesDict:
            for item, value in speciesDict[self['species']].items():
                if item not in data:
                    self[item] = value
