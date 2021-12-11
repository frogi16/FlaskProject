from backend.db import db_query

class Body:
    def __init__(self, name, labels, orbits):
        self.name = name
        if "Body" not in labels:
            labels.append("Body")
        self.labels = labels
        self.labels_str = ':'.join([""] + [f"`{l}`" for l in labels])
        self.orbits = orbits

    @staticmethod
    def get_all():
        result = db_query(f"MATCH (a:Body) RETURN a")
        return result

    def exists(self):
        result = db_query(f"MATCH (a{self.labels_str} {{name: '%s'}}) RETURN a" % (self.name))
        return len(result) > 0

    def add(self):
        if self.exists():
            raise ValueError(f"{self.name} already exists")

        res = db_query(f"CREATE (a{self.labels_str} {{name: '%s'}}) RETURN a" % (self.name))
        if len(res) == 0:
            raise ValueError("Couldn't create object")

        return res

    def add_orbits_relationship(self):
        res = db_query(f"MATCH (a{self.labels_str}), (b:Body) WHERE a.name = '{self.name}' AND b.name = '{self.orbits}' CREATE (a)-[r:ORBITS]->(b) RETURN type(r)")
        if len(res) == 0:
            raise ValueError("Couldn't create relationship")

        return res

    def delete(self):
        if self.exists():
            return db_query(f"MATCH (a{self.labels_str} {{name: '%s'}}) DETACH DELETE a" % (self.name))
        return False