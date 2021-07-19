from Utilitai.OsupMAJ.platine import Carac_chevilles

class AdmissiblePlatine():
    def __init__(self,data):
        self.carac_chevilles = Carac_chevilles(data)
        self.e = data['platine']['e']
        self.l = data['platine']['l']
        nbCheville = data['platine']['nbCheville']
        self.d = self.get_diffusion_length(nbCheville)

    def get_diffusion_length(self,nbCheville):
        d = []
        for i in range(len(nbCheville)):
            if nbCheville[i] == "2":
                d.append(self.carac_chevilles.carac2chevilles(i))
            else:
                d.append(self.carac_chevilles.carac4chevilles(i))
        return d


    def cm2Chevilles(self,Fx, Fy, Fz, Mx, My, Mz,i):
        """
        Gives membrane stress for 2 dowels plate
        """
        print("carac cheville",[self.carac_chevilles.cisaillement2chev(Fx, Fy, Fz, Mx, My, Mz,i),self.d[i],self.e[i]])
        Cm = self.carac_chevilles.cisaillement2chev(Fx, Fy, Fz, Mx, My, Mz,i)/(self.d[i][1]*float(self.e[i]))
        print("Cm", Cm)
        return Cm

    def cm4chevilles(self,Fx, Fy, Fz, Mx, My, Mz,i):
        """
        Gives membrane stress for 4 dowels plate
        """
        # 4  dowels plate has 2 diffusion length we take max result
        Cm = self.carac_chevilles.cisaillement4chev(Fx, Fy, Fz, Mx, My, Mz,i)/(self.d[i][1]*float(self.e[i]))
        print("Cm", Cm)
        return Cm

    def flex2chevilles(self,Fx, Fy, Fz, Mx, My, Mz,i):
        """
        Gives flexion stress for 2 dowels plate
        """
        Cb = self.carac_chevilles.traction2chev(Fx, Fy, Fz, Mx, My, Mz,i)*self.d[i][0]*6/(self.d[i][1]*float(self.e[i])**2)
        print("Traction", self.carac_chevilles.traction2chev(Fx, Fy, Fz, Mx, My, Mz,i))
        print("Cb", Cb)
        return Cb

    def flex4chevilles(self,Fx, Fy, Fz, Mx, My, Mz,i):
        Cb = self.carac_chevilles.traction4chev(Fx, Fy, Fz, Mx, My, Mz,i)*self.d[i][0]*6/(self.d[i][1]*float(self.e[i])**2)
        return Cb