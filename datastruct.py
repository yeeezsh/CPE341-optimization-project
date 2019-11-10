from pprint import pprint


def readfile(path):
    f = open(path, "r")
    content = f.read()
    return content


def parse_csv(data=''):
    line = data.splitlines()  # split each line to list
    result = []
    for i in line:
        row = i.split(',')  # split each row to sub list
        result.append(row)
    return result[1:]  # cut header out


def parse_matrix_dist(data='', reversible=False):
    parse = data.splitlines()
    result = []
    if reversible:
        # if parse reversible file
        for r, e in enumerate(parse):  # append data to result first
            result.append(e.split('\t'))
        for r, re in enumerate(result):  # transpose matrix
            if r > 0:
                for c, ce in enumerate(re):
                    result[r][c] = result[c][r]
                    if ce == '0':  # if found 0 brake transpose op
                        break
        return result
    else:
        for e in parse:  # split by tab
            result.append(e.split('\t'))
        return result


class Place:
    def __init__(self, _data):
        self.node = {}
        self.matrix = {}
        for i in _data:
            self.node[i[0]] = {
                "name": i[1],
                "lat": i[2],
                "lng": i[3]
            }

    def show_place(self):
        print(self.node)

    def show_matrix(self):
        print('show matrix')
        pprint(self.matrix)

    def add_matrix(self, data, name='', field=[]):      # for adding matrix relation
        if len(self.node.keys()) == 0:
            return Exception('must declare with place data fist')
        self.matrix[name] = []
        for e in data:
            row = []
            for i, n in enumerate(e):
                contain = n.split(',')
                mapping = {}
                if contain[0] != '0':
                    for fi, f in enumerate(field):      # loop through fields for setting data struct for each node
                        mapping[f] = float(contain[fi])
                else:
                    for fi, f in enumerate(field):      # if found 0 set everything in dict = 0
                        mapping[f] = float(0)
                row.append(mapping)
            self.matrix[name].append(row)               # append mapping to self class

    def transit_info_id(self, type_of_transit, start, stop):
        return self


DATA_FIELD = ['dist', 'time', 'cost']
place = readfile('place.csv')
place = parse_csv(place)
# print(place)

dist_public = readfile('dist.public.txt')
dist_public = parse_matrix_dist(dist_public)
# print(dist_public)


node = Place(place)
node.add_matrix(dist_public, 'public', DATA_FIELD)
# node.show_matrix()
# test = node.matrix.get('public')
# print(test)
# print(test[0][2])
# node.show_place()

dist_taxi = readfile('dist.taxi.txt')
dist_taxi = parse_matrix_dist(dist_taxi, True)
node.add_matrix(dist_taxi, 'taxi', DATA_FIELD)

node.show_matrix()
