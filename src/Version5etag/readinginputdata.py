from src.Version5etag.database import Database


class ReadingInputData:
    def __init__(self, data_dowel):
        print('data', data_dowel)
        self.gammedowel = data_dowel.get("gamme")
        self.typedowel = data_dowel.get("type")
        self.modeledowel = data_dowel.get("modele")
        self.hef = data_dowel.get("hef")
        self.norme = data_dowel.get("norme")
        self.tfix = data_dowel.get("tfix")
        self.nom = []
        self.opendata = Database().open_database()
        self.datadowelosup = self.opendata.get("datadowel")
        self.typebeton = data_dowel.get("typebeton")
        self.fulldata = self.get_dowel_data()

        self.read_input_data()

    def read_input_data(self):
        global scrn, ccrN
        gamme = self.modeledowel
        fck = self.get_concrete_property('fck')

        if gamme == "HSL 3-G" or gamme == "HST3":
            scrn = 3 * self.hef
            ccrN = 1.5 * self.hef

        elif gamme == "HDA-T" or gamme == "HDA-P" or gamme == "W-HAZ-B" or gamme == "W-FAZ" or gamme == "FIX Z XTREM" \
                or gamme == "TRIGA XTREM":
            scrn = float(self.get_dowel_property('Rupture par cone beton et par fendage - espacement scr,N (mm)'))
            ccrN = float(self.get_dowel_property('Rupture par cone beton et par fendage - distance au bord ccr,N (mm)'))

        scrsp = float(self.get_dowel_property('Rupture par fendage - espacement scr,sp (mm)'))
        ccrsp = float(self.get_dowel_property('Rupture par fendage - distance au bord ccr,sp (mm)'))

        if gamme == "HSL 3-G" or gamme == "HST3" or gamme == "W-HAZ-B" or gamme == "W-FAZ" or gamme == "FIX Z XTREM" \
                or gamme == "TRIGA XTREM":
            self.hmin = float(self.get_dowel_property('Epaisseur mini du support hmin,i (mm)'))
        elif gamme == "HDA-T" or gamme == "HDA-P":
            self.hmin = float(self.get_dowel_property('Epaisseur mini du support hmin,i (mm)')) - self.tfix

        Es = float(self.get_dowel_property('Module elasticite acier Es (N/mm2)'))
        Eb = self.get_concrete_property('Module elasicite beton Eb')
        self.nd = Es / Eb
        Ar = float(self.get_dowel_property('Section resistante As (mm2)'))
        k8 = float(self.get_dowel_property('Rupture du beton par effet de levier - facteur de pry out k3'))
        aeq_isolee = float(self.get_dowel_property('aeq - isolee'))
        aeq_groupe = float(self.get_dowel_property('aeq - groupe'))
        return {"scrn": scrn,
                "ccrN": ccrN,
                "scrsp": scrsp,
                "ccrsp": ccrsp,
                "hmin": self.hmin,
                "nd": self.nd,
                "Ar": Ar,
                "fck": fck,
                "k8": k8,
                "aeq_groupe": aeq_groupe,
                "aeq_isolee": aeq_isolee}

    def data_recovery(self, malist, donnee, dico):
        malist = []
        for h in dico:
            malist.append(h.get("{}".format(donnee)))
        return malist

    def get_dowel_data(self):
        return self.datadowelosup[self.gammedowel][self.modeledowel][self.typedowel][str(self.hef)]

    def get_dowel_property(self, propriete):
        return self.fulldata['{}'.format(propriete)]

    def get_dowel_full_property(self):
        return {
            "smin": float(self.get_dowel_property('Entraxe minimum smin (mm)')),
            "c_smin": float(self.get_dowel_property('Entraxe minimum c >= (mm)')),
            "cmin": float(self.get_dowel_property('Distance au bord minimum cmin (mm)')),
            "s_cmin": float(self.get_dowel_property('Distance au bord minimum s >= (mm)')),
            "dmin": float(self.get_dowel_property('Distance minimum au bord de la platine (mm)')),
            "tmin": float(self.get_dowel_property('Epaisseur a fixer tfix1 (mm)')),
            "tmax": float(self.get_dowel_property('Epaisseur a fixer tfix2 (mm)'))
        }

    def get_concrete_property(self, propriete):
        if self.norme == "ETAG":
            self.dataconcrete = self.opendata.get("dataconcrete_etag")
        else:
            self.dataconcrete = self.opendata.get("dataconcrete_ec2")
        q = self.data_recovery(self.nom, "Classe de resistance", self.dataconcrete).index(self.typebeton)
        prop = self.dataconcrete[q]['{}'.format(propriete)]
        return prop
