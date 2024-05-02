from abc import ABC


class Mappable(ABC):
    def ToDictionary(self, *, includeOnly=None, **kwargs):
        def value(x):
            if issubclass(type(x), Mappable): x = x.ToDictionary(includeOnly=kwargs.get(type(x).__name__, None))
            elif type(x) == dict: x = {key: value(val) for key, val in x.items()}
            elif type(x) in [tuple, list, set]: x = type(x)(value(val) for val in x)
            return x
        includeOnly = includeOnly if includeOnly else self.Properties()
        return {name: value(getattr(self, name)) for name in includeOnly}

    def Properties(self):
        return [name for name in dir(self) if not name.startswith('_') and not callable(getattr(self, name))]

    def FromDictionary(self, data):
        self.__dict__.update(data)
        return self
