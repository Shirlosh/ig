import json
import uuid

import pandas as pd


def PrintDictionary(d):
    print(json.dumps(d, indent=2))


def ListDictionaryValues(d):
    l = []
    for key in d:
        if type(d[key]) == dict: l.extend(ListDictionaryValues(d[key]))
        elif type(d[key]) == list: l.extend(d[key])
        else: l.append(d[key])
    return l


def ExportJSON(d, file):
    open(file, "w").write(json.dumps(d))


def ImportJSON(file):
    return json.load(open(file, 'r'))

def ImportExcelToDictionary(file):
    df = pd.read_excel(file)
    Edges, Vertices = {}, {}
    d = df.iterrows()

    for index, row in d:
        source, target = str(row['Site A Latitude']) + ';' + str(row['Site A Longitude']), str(row['Site B Latitude']) + ';' + str(row['Site B Longitude'])
        Vertices[source] = Vertices.get(source, uuid.uuid4().hex)
        Vertices[target] = Vertices.get(target, uuid.uuid4().hex)
        Edges[uid] = {'ID': (uid := uuid.uuid4().hex),
                      'Source': {'ID': Vertices[source], 'Location': (float(row['Site A Latitude']), float(row['Site A Longitude']))},
                      'Target': {'ID': Vertices[target], 'Location': (float(row['Site B Latitude']), float(row['Site B Longitude']))}
                      #     'Frequency': row['Site A Frequency']
                      #     "MaxPt": dBmToMW(float(row['Power'])),
                      }
    return {'Edges': Edges}


def SaveDictToExcel(d, file):
    pd.read_json(json.dumps(d)).to_excel(file)
