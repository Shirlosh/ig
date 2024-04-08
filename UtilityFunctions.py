def ListDictionaryValues(d):
    l = []
    for key in d:
        if type(d[key]) == dict: l.extend(ListDictionaryValues(d[key]))
        if type(d[key]) == list: l.extend(d[key])
        else: l.append(d[key])
    return l
