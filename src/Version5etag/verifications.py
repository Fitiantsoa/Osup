
class Verification:
    def __init__(self, inertia, data, readinputdata, data_dowel):
        self.Lx = data_dowel.get("Lx")
        self.Lz = data_dowel.get("Lz")
        self.h = float(data_dowel.get("h"))
        self.NbFixa = data_dowel.get("nbCheville")
        self.sx0 = self.sx(data_dowel.get("sx0"), data_dowel.get("sz0"))[0]
        self.sx1 = 0
        self.sz0 = self.sx(data_dowel.get("sx0"), data_dowel.get("sz0"))[1]
        self.sz1 = 0
        self.cx0 = data_dowel.get("cx0")
        self.cx1 = data_dowel.get("cx1")
        self.cz0 = data_dowel.get("cz0")
        self.cz1 = data_dowel.get("cz1")
        self.hef = data_dowel.get("hef")
        self.modele = data_dowel.get("dowelname")
        self.typecharge = data_dowel.get("TypeCharge")
        self.smin = data.get("smin")
        self.c_smin = data.get("c_smin")
        self.cmin = data.get("cmin")
        self.s_cmin = data.get("s_cmin")
        self.s = inertia.get("s")
        self.c = inertia.get("c")
        self.dmin = data.get("dmin")
        self.tmin = data.get("tmin")
        self.tmax = data.get("tmax")
        self.tfix = data_dowel.get("tfix")
        self.hmin = readinputdata.get("hmin")
        self.dx0 = data_dowel.get("dx0")
        self.dx1 = data_dowel.get("dx1")
        self.dz0 = data_dowel.get("dz0")
        self.dz1 = data_dowel.get("dz1")

    def sx(self, sx0, sz0):
        if self.NbFixa == 2:
            if sx0 == "":
                sx0 = 0
                return sx0, sz0
            if sz0 == "":
                sz0 = 0
                return sx0, sz0
        else:
            return sx0, sz0

    def verification_anchors(self):
        if self.verification_entraxe_edge() is True and self.verification_center_distance_edge() is True and \
                self.verification_dimension_board() is True and self.verification_tfix() is True and \
                self.verification_h() is True and self.verification_type_cheville() is True:
            print("Ancrages définis")
            return True
        else:
            print("Ancrages non définis")
            return False

    def verification_input(self):
        if self.Lx == 0 or self.Lz == 0:
            print("Saisie incomplète : veuillez rentrer les dimensions de la platine")
            return False
        if self.h == 0:
            print("Saisie incomplète : veuillez rentrer une épaisseur de béton")
            return False
        if self.NbFixa == 4:
            if self.sx0 == 0 or self.sz0 == 0:
                print("Saisie incomplète : veuillez rentrer les entraxes correspondantes au nombre de chevilles")
                return False
        elif self.NbFixa == 2:
            if self.sx0 == 0:
                print("Saisie incomplète : veuillez rentrer les entraxes correspondantes au nombre de chevilles")
                return False
        if self.cx0 == 0 or self.cx1 == 0 or self.cz1 == 0 or self.cz0 == 0:
            print("Saisie incomplète : veuillez rentrer les distances au bord correspondantes")
            return False
        return True

    def verification_center_distance_edge(self):
        if self.s < self.smin or self.c < self.cmin or (self.s < self.s_cmin and self.c < self.c_smin):
            if self.s < self.smin:
                print("Erreur : entraxe trop faible (smin= {} mm)".format(self.smin))
                return False
            if self.c < self.smin:
                print("Erreur : distance au bord trop faible (cmin= {} mm)".format(self.cmin))
                return False
            if self.s < self.s_cmin and self.c < self.c_smin:  # TODO : Condition à faire faux sur VBA
                return False
        return True

    def verification_dimension_board(self):
        if self.Lx < self.sx0 + self.sx1 + 2 * self.dmin or self.Lz < self.sz0 + self.sz1 + 2 * self.dmin:
            if self.Lx < self.sx0 + self.sx1 + 2 * self.dmin:
                print("Erreur : dimension Lx de la platine trop faible (Lx>= {} mm)"
                      .format((self.sx0 + self.sx1 + 2 * self.dmin)))
                return False
            elif self.Lz < self.sz0 + self.sz1 + 2 * self.dmin:
                print("Erreur : dimension Lx de la platine trop faible (Lx>= {} mm)"
                      .format((self.sz0 + self.sz1 + 2 * self.dmin)))
            return False

        if self.dx0 < self.dmin or self.dx1 < self.dmin or self.dz0 < self.dmin or self.dz1 < self.dmin:
            if self.dx0 < self.dmin or self.dx1 < self.dmin:
                print("Erreur : distance entre les fixations et le bord de la platine trop faible (dx>= {} mm)".format(
                    self.dmin))
                return False
            elif self.dz0 < self.dmin or self.dz1 < self.dmin:
                print("Erreur : distance entre les fixations et le bord de la platine trop faible (dz>= {} mm)".format(
                    self.dmin))
                return False

        if self.dx0 > self.cx0 or self.dx1 > self.cx1:
            if self.dx0 > self.cx0:
                print(
                    "Erreur : dimension Lx de la platine trop importante (dx<= {} mm) ou distance au bord trop faible"
                    "(cx>= {} mm)".format(
                        self.cx0, self.dx0))
                return False
            elif self.dx1 > self.cx1:
                print(
                    "Erreur : dimension Lx de la platine trop importante (dx<= {} mm) ou distance au bord trop faible"
                    "(cx>= {} mm)".format(
                        self.cx1, self.dx1))
                return False

        if self.dz0 > self.cz0 or self.dz1 > self.cz1:
            if self.dz0 > self.cz0:
                print(
                    "Erreur : dimension Lz de la platine trop importante (dz<= {} mm) ou distance au bord trop faible "
                    "(cz>= {} mm)".format(
                        self.cz0, self.dz0))
                return False
            elif self.dz1 > self.cz1:
                print(
                    "Erreur : dimension Lz de la platine trop importante (dz<= {} mm) ou distance au bord trop "
                    "faible(cz>= {} mm)".format(
                        self.cz1, self.dz1))
                return False
        return True

    def verification_tfix(self):

        if self.tfix < self.tmin:
            print("Erreur : platine pas suffisament épaisse pour ce modèle de cheville (tmin= {} mm)".format(self.tmin))
            return False

        if self.tfix > self.tmax:
            print("Erreur : platine trop épaisse pour ce modèle de cheville (tmax= {} mm)".format(self.tmax))
            return False
        return True

    def verification_h(self):
        if self.h < self.hmin:
            print("Erreur : béton pas suffisament épais pour ce modèle de cheville et cette profondeur d'ancrage"
                  "(hmin= {} mm)".format(self.hmin))
            return False
        return True

    def verification_type_cheville(self):
        if (self.typecharge == "Sismique C2" and (self.modele == "HILTI HSL 3-G M8" or self.modele ==
                                                  "HILTI HSL 3-G M24" or self.modele == "TRIGA Z XTREM E8-12" or
                                                  self.modele == "TRIGA Z XTREM E20-28" or self.modele == "SPIT FIX Z XTREM M8" or
                                                  (self.modele == "HILTI HST3 M10" and self.hef == 40) or (self.modele ==
                                                  "HILTI HST3 M16" and self.hef == 65) or self.modele == "HILTI HST3 M24" or
                                                  self.modele == "Würth W-HAZ-B M6")):
            print("Ce modèle de fixation n'est pas utilisable pour des charges de catégorie sismique C2")
            return False
        else:
            return True

    def verification_entraxe_edge(self):
        #print(self.s,  self.smin, self.c, self.cmin, self.s_cmin, self.c_smin)
        if self.s < self.smin or self.c < self.cmin or (self.s < self.s_cmin and self.c < self.c_smin):
            if self.s < self.smin:
                print("Erreur : entraxe trop faible (smin= {} mm)".format(self.smin))
                return False

            if self.c < self.cmin:
                print("Erreur : distance au bord trop faible (cmin= {} mm)".format(self.cmin))
                return False

            if self.s < self.s_cmin and self.c < self.c_smin:
                if self.cx0 < self.c_smin - 0.5 * (self.sx0 - self.smin) or self.sx0 < self.s_cmin - 2 * (self.cx0 - self.cmin):
                    print("Erreur : entraxe et distance au bord trop faibles (sx>= {} mm ou cx>= {} mm)".format(
                        self.s_cmin - 2 * (self.cx0 - self.cmin), self.c_smin - 0.5 * (self.sx0 - self.smin)))
                    return False

                if self.NbFixa == 4:
                    if self.sx0 != 0 and self.sx1 != 0:
                        if self.cx1 < (self.c_smin - 0.5 * (self.sx0 - self.smin)) or self.sx1 < self.s_cmin - 2 *\
                                (self.cx1 - self.cmin):
                            print("Erreur : entraxe et distance au bord trop faibles (sx>= {} mm ou cx>= {} mm)".format(
                                self.s_cmin - 2 * (self.cx0 - self.cmin), self.c_smin - 0.5 * (self.sx0 - self.smin)))
                            return False

                        if self.sz0 != 0:
                            if self.cz0 < self.c_smin - 0.5 * (self.sz0 - self.smin) or self.sz0 < self.s_cmin - 2 * (
                                    self.cz0 - self.cmin):
                                print("Erreur : entraxe et distance au bord trop faibles (sz>= {} mm ou cz>= {} mm)"
                                      .format(self.s_cmin - 2 * (self.cz0 - self.cmin), self.c_smin - 0.5 * (self.sz0 -
                                                                                                             self.smin)))
                                return False

                        if self.sz1 != 0:
                            if self.cz1 < self.c_smin - 0.5 * (self.sz1 - self.smin) or self.sz1 < self.s_cmin - 2 * (self.cz1 - self.cmin):
                                print("Erreur : entraxe et distance au bord trop faibles (sz>= {} mm ou cz>= {} mm)".format(self.s_cmin - 2 * (self.cz1 - self.cmin), self.c_smin - 0.5 * (self.sz1 - self.smin)))
                                return False
        return True