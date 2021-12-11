from neo4j import GraphDatabase

class Db:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query):
        def cypher_read(tx, cypher):
            return [r.values() for r in tx.run(cypher)]

        with self.driver.session() as session:
            return session.read_transaction(cypher_read, query)


uri = "neo4j+s://bdc6b40d.databases.neo4j.io"
user = "neo4j"
password = "IPp0x7S-FIgscKTwPWUaEuoQ5JelXq47XCIiCpamW3A"
db = Db(uri, user, password)

def db_query(query):
    return db.query(query)

def get_labels():
    return db_query("call db.labels()")