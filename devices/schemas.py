class Serializable:
    serializer = None

    def dumps(self):
        return self.serializer.dumps(self)

    def dump(self):
        return self.serializer.dump(self)

    @classmethod
    def loads(cls, json_data):
        return cls.serializer.loads(json_data)

    @classmethod
    def load(cls, json):
        return cls.serializer.load(json)
