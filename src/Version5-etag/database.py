import json


class Database:
    def open_database(self):
        with open("doweldatabase.json", "r") as f:
            datadowel = json.load(f)

        with open("concretedatabase.json", "r") as f:
            dataconcrete_ec2 = json.load(f)

        with open("concretedatabaseetag.json", "r") as f:
            dataconcrete_etag = json.load(f)

        return {"dataconcrete_ec2": dataconcrete_ec2,
                "dataconcrete_etag": dataconcrete_etag,
                "datadowel": datadowel
                }
