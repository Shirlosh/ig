import json
import pandas as pd


def ListDictionaryValues(d):
    l = []
    for key in d:
        if type(d[key]) == dict: l.extend(ListDictionaryValues(d[key]))
        if type(d[key]) == list: l.extend(d[key])
        else: l.append(d[key])
    return l


def ExportJSON(d, file):
    open(file, "w").write(json.dumps(d))


def ImportJSON(file):
    return json.load(open(file, 'r'))


def SaveDictToExcel(d, file):
    pd.read_json(json.dumps(d)).to_excel(file)
