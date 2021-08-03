from src.constantes import DOWEL_DB, CONCRETE_DB, CONCRETE_ETAG_DB
from src.utils import read_json


class Database:
    def __init__(self):
        self.dowel_db = read_json(DOWEL_DB)
        self.dataconcrete_ec2 = read_json(CONCRETE_DB)
        self.dataconcrete_etag = read_json(CONCRETE_ETAG_DB)

    def open_database(self):
        return {"dataconcrete_ec2": self.dataconcrete_ec2,
                "dataconcrete_etag": self.dataconcrete_etag,
                "datadowel": self.dowel_db
                }