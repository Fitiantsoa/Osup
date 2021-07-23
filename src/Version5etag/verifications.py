
class Verification:
    def __init__(self, inertia, data, readinputdata, data_dowel):
        self.Lx = data_dowel.get("Lx")
        self.Lz = data_dowel.get("Lz")
        self.h = data_dowel.get("h")
        self.NbFixa = data_dowel.get("nbCheville")
        self.sx0 = data_dowel.get("sx0")
        self.sx1 = 0
        self.sz0 = data_dowel.get("sz0")
        self.sz1 = 0
        self.cx0 = data_dowel.get("cx0")
        self.cx1 = data_dowel.get("cx1")
        self.cz0 = data_dowel.get("cz0")
        self.cz1 = data_dowel.get("cz1")
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
        self.verification_anchors()

    def verification_anchors(self):
        self.verification_input()
        self.verification_center_distance_edge()
        self.verification_dimension_board()
        self.verification_tfix()
        self.verification_h()
        self.verification_entraxe_edge()
        if self.ok3 is True:
            print("Ancrages définis")
            ancrage = "oui"
        else:
            print("Ancrages non définis")
            ancrage = "non"
        return ancrage

    def verification_input(self):
        if self.Lx == 0 or self.Lz == 0:
            print("Saisie incomplète : veuillez rentrer les dimensions de la platine")
        if self.h == 0:
            print("Saisie incomplète : veuillez rentrer une épaisseur de béton")
        if self.NbFixa == 4:
            if self.sx0 == 0 or self.sz0 == 0:
                print("Saisie incomplète : veuillez rentrer les entraxes correspondantes au nombre de chevilles")
        elif self.NbFixa == 2:
            if self.sx0 == 0:
                print("Saisie incomplète : veuillez rentrer les entraxes correspondantes au nombre de chevilles")

        if self.cx0 == 0 or self.cx1 == 0 or self.cz1 == 0 or self.cz0 == 0:
            print("Saisie incomplète : veuillez rentrer les distances au bord correspondantes")

    def verification_center_distance_edge(self):

        if self.s < self.smin or self.c < self.cmin or (self.s < self.s_cmin and self.c < self.c_smin):
            if self.s < self.smin:
                print("Erreur : entraxe trop faible (smin= {} mm)".format(self.smin))
            if self.c < self.smin:
                print("Erreur : distance au bord trop faible (cmin= {} mm)".format(self.cmin))
            if self.s < self.s_cmin and self.c < self.c_smin:
                pass  # A faire

    def verification_dimension_board(self):

        if self.Lx < self.sx0 + self.sx1 + 2 * self.dmin or self.Lz < self.sz0 + self.sz1 + 2 * self.dmin:
            if self.Lx < self.sx0 + self.sx1 + 2 * self.dmin:
                print("Erreur : dimension Lx de la platine trop faible (Lx>= {} mm)"
                      .format((self.sx0 + self.sx1 + 2 * self.dmin)))
            elif self.Lz < self.sz0 + self.sz1 + 2 * self.dmin:
                print("Erreur : dimension Lx de la platine trop faible (Lx>= {} mm)"
                      .format((self.sz0 + self.sz1 + 2 * self.dmin)))

        if self.dx0 < self.dmin or self.dx1 < self.dmin or self.dz0 < self.dmin or self.dz1 < self.dmin:
            if self.dx0 < self.dmin or self.dx1 < self.dmin:
                print("Erreur : distance entre les fixations et le bord de la platine trop faible (dx>= {} mm)".format(
                    self.dmin))
            elif self.dz0 < self.dmin or self.dz1 < self.dmin:
                print("Erreur : distance entre les fixations et le bord de la platine trop faible (dz>= {} mm)".format(
                    self.dmin))

        if self.dx0 > self.cx0 or self.dx1 > self.cx1:
            if self.dx0 > self.cx0:
                print(
                    "Erreur : dimension Lx de la platine trop importante (dx<= {} mm) ou distance au bord trop faible"
                    "(cx>= {} mm)".format(
                        self.cx0, self.dx0))
            elif self.dx1 > self.cx1:
                print(
                    "Erreur : dimension Lx de la platine trop importante (dx<= {} mm) ou distance au bord trop faible"
                    "(cx>= {} mm)".format(
                        self.cx1, self.dx1))

        if self.dz0 > self.cz0 or self.dz1 > self.cz1:
            if self.dz0 > self.cz0:
                print(
                    "Erreur : dimension Lz de la platine trop importante (dz<= {} mm) ou distance au bord trop faible "
                    "(cz>= {} mm)".format(
                        self.cz0, self.dz0))
            elif self.dz1 > self.cz1:
                print(
                    "Erreur : dimension Lz de la platine trop importante (dz<= {} mm) ou distance au bord trop "
                    "faible(cz>= {} mm)".format(
                        self.cz1, self.dz1))

    def verification_tfix(self):

        if self.tfix < self.tmin:
            print("Erreur : platine pas suffisament épaisse pour ce modèle de cheville (tmin= {} mm)".format(self.tmin))

        if self.tfix > self.tmax:
            print("Erreur : platine trop épaisse pour ce modèle de cheville (tmax= {} mm)".format(self.tmax))

    def verification_h(self):
        if self.h < self.hmin:
            print("Erreur : béton pas suffisament épais pour ce modèle de cheville et cette profondeur d'ancrage"
                  "(hmin= {} mm)".format(self.hmin))

    def verification_entraxe_edge(self):
        #print(self.s,  self.smin, self.c, self.cmin, self.s_cmin, self.c_smin)
        if self.s < self.smin or self.c < self.cmin or (self.s < self.s_cmin and self.c < self.c_smin):
            if self.s < self.smin:
                print("Erreur : entraxe trop faible (smin= {} mm)".format(self.smin))
                self.ok3 = False
                return self.ok3
            self.ok3 = True

            if self.c < self.cmin:
                print("Erreur : distance au bord trop faible (cmin= {} mm)".format(self.cmin))
                self.ok3 = False
                return self.ok3
            self.ok3 = True

            if self.s < self.s_cmin and self.c < self.c_smin:
                if self.cx0 < self.c_smin - 0.5 * (self.sx0 - self.smin) or self.sx0 < self.s_cmin - 2 * (self.cx0 - self.cmin):
                    print("Erreur : entraxe et distance au bord trop faibles (sx>= {} mm ou cx>= {} mm)".format(
                        self.s_cmin - 2 * (self.cx0 - self.cmin), self.c_smin - 0.5 * (self.sx0 - self.smin)))
                    self.ok3 = False
                    return self.ok3
                self.ok3 = True

                if self.NbFixa == 4:
                    if self.sx0 != 0 and self.sx1 != 0:
                        if self.cx1 < (self.c_smin - 0.5 * (self.sx0 - self.smin)) or self.sx1 < self.s_cmin - 2 *\
                                (self.cx1 - self.cmin):
                            print("Erreur : entraxe et distance au bord trop faibles (sx>= {} mm ou cx>= {} mm)".format(
                                self.s_cmin - 2 * (self.cx0 - self.cmin), self.c_smin - 0.5 * (self.sx0 - self.smin)))
                            self.ok3 = False
                            return self.ok3
                        self.ok3 = True

                        if self.sz0 != 0:
                            if self.cz0 < self.c_smin - 0.5 * (self.sz0 - self.smin) or self.sz0 < self.s_cmin - 2 * (
                                    self.cz0 - self.cmin):
                                print("Erreur : entraxe et distance au bord trop faibles (sz>= {} mm ou cz>= {} mm)"
                                      .format(self.s_cmin - 2 * (self.cz0 - self.cmin), self.c_smin - 0.5 * (self.sz0 -
                                                                                                             self.smin))
                                      )
                                self.ok3 = False
                                return self.ok3
                            self.ok3 = True

                        if self.sz1 != 0:
                            if self.cz1 < self.c_smin - 0.5 * (self.sz1 - self.smin) or self.sz1 < self.s_cmin - 2 * (self.cz1 - self.cmin):
                                print("Erreur : entraxe et distance au bord trop faibles (sz>= {} mm ou cz>= {} mm)".format(self.s_cmin - 2 * (self.cz1 - self.cmin), self.c_smin - 0.5 * (self.sz1 - self.smin)))
                                self.ok3 = False
                                return self.ok3
                            self.ok3 = True
        self.ok3 = True
        return self.ok3