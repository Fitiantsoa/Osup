import json


def read_json(path):
    with open(path) as f:
        return json.loads(f.read())


def sort_beam_by(beams, k1, k2=None):
    sorted_dict = {}
    for beam in beams:
        key = beam[k1]
        if k2 is not None:
            key += ' ' + beam[k2]
        if key not in list(sorted_dict.keys()):
            sorted_dict[key] = [beam['id']]
        else:
            sorted_dict[key].append(beam['id'])
    return sorted_dict


def lerp(Y1, Y2, X1, X2, X):
    return Y1 + (X - X1) * ((Y2 - Y1) / (X2 - X1))