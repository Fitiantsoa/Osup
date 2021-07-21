from src.constantes import *


class ReadingInputData:
    def __init__(self, hef, tfix, modele, typebeton, norme):
        self.hef = hef
        self.norme = norme
        self.tfix = tfix
        self.modele = modele
        self.nom = []
        self.opendata = self.open_database()
        self.datadowel = self.opendata.get("datadowel")
        self.typebeton = typebeton
        self.fulldata = self.get_dowel_data()
        self.read_input_data()

    def read_input_data(self):
        global scrn, ccrN
        gamme = self.get_dowel_property('gamme')
        fck = self.get_concrete_property('fck')

        if gamme == "HSL 3-G" or gamme == "HST3":
            scrn = 3 * self.hef
            ccrN = 1.5 * self.hef

        elif gamme == "HDA-T" or gamme == "HDA-P" or gamme == "W-HAZ-B" or gamme == "W-FAZ" or gamme == "FIX Z XTREM" \
                or gamme == "TRIGA XTREM":
            scrn = self.get_dowel_property('rupture cone beton fendage espacement')
            ccrN = self.get_dowel_property('rupture cone beton fendage distance au bord')

        scrsp = self.get_dowel_property('rupture fendage espacement')
        ccrsp = self.get_dowel_property('rupture fendage distance bord')

        if gamme == "HSL 3-G" or gamme == "HST3" or gamme == "W-HAZ-B" or gamme == "W-FAZ" or gamme == "FIX Z XTREM" \
                or gamme == "TRIGA XTREM":
            self.hmin = self.get_dowel_property('epaisseur mini du support hmin')
        elif gamme == "HDA-T" or gamme == "HDA-P":
            self.hmin = self.get_dowel_property('epaisseur mini du support hmin') - self.tfix

        Es = self.get_dowel_property('module elasticite')
        Eb = self.get_concrete_property('Module elasicite beton Eb')
        self.nd = Es / Eb
        Ar = self.get_dowel_property('section resistante a s')
        return scrn, ccrN, scrsp, ccrsp, self.hmin, self.nd, Ar, fck

    def data_recovery(self, malist, donnee, dico):
        malist = []
        for h in dico:
            malist.append(h.get("{}".format(donnee)))
        return malist

    def get_dowel_data(self):
        listq = []
        q = self.data_recovery(self.nom, "nom", self.datadowel).index(
            '{}'.format(self.modele))  # Index dépend du choix utilisateur
        for j in range(3):
            listq.append(self.datadowel[q + j])
        r = self.data_recovery(self.hef, "profondeur encrage", listq).index(self.hef)
        fulldatadowel = self.datadowel[q + r]
        return fulldatadowel

    def get_dowel_property(self, propriete):
        prop = self.fulldata['{}'.format(propriete)]
        return prop

    def get_dowel_full_property(self):
        return {
            "smin": self.get_dowel_property('entraxe mini mums min'),
            "c_smin": self.get_dowel_property('entraxe mini mumc'),
            "cmin": self.get_dowel_property('distance bord mini cmin'),
            "s_cmin": self.get_dowel_property('distance bord mini s'),
            "dmin": self.get_dowel_property('distance mini bord platine'),
            "tmin": self.get_dowel_property('epaisseur a fixer tfix'),
            "tmax": self.get_dowel_property('epaisseur a fixer tfix2'),
        }

    def get_concrete_property(self, propriete):
        if self.norme == "ETAG":
            self.dataconcrete = self.opendata.get("dataconcrete_etag")
        else:
            self.dataconcrete = self.opendata.get("dataconcrete_ec2")
        q = self.data_recovery(self.nom, "Classe de resistance", self.dataconcrete).index(self.typebeton)
        prop = self.dataconcrete[q]['{}'.format(propriete)]
        return prop

    # def open_database(self):
    #     with open(DOWEL_DB, "r") as f:
    #         datadowel = json.load(f)
    #
    #     with open("concretedatabase.json", "r") as f:
    #         dataconcrete_ec2 = json.load(f)
    #
    #     with open("concretedatabaseetag.json", "r") as f:
    #         dataconcrete_etag = json.load(f)
    #
    #     return {"dataconcrete_ec2": dataconcrete_ec2,
    #             "dataconcrete_etag": dataconcrete_etag,
    #             "datadowel": datadowel
    #             }