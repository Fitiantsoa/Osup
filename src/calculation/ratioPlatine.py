from Utilitai.OsupMAJ.platine import Carac_chevilles
from Utilitai.OsupMAJ.contraintePlatine import AdmissiblePlatine

class RatioPlatine():
    def __init__(self,data):
        self.carac_chevilles = Carac_chevilles(data)

        self.coefDuct = data['platine']['coefDuct']
        self.SyPlatine = data['platine']['Sy']
        self.SuPlatine = data['platine']['Su']
        self.SPlatine = data['platine']['S']
        self.adm_platine = AdmissiblePlatine(data)




    def ratio2chevilles(self,niveau,Fx, Fy, Fz, Mx, My, Mz,i):
        f = open("C:\\Users\\fitiantsoa.antenaina\\Desktop\\aster\\result.txt", "a")
        ratio = (self.adm_platine.cm2Chevilles(Fx[i], Fy[i], Fz[i], abs(Mx[i]), abs(My[i]), abs(Mz[i]),i)+self.adm_platine.flex2chevilles(Fx[i], Fy[i], Fz[i], abs(Mx[i]), abs(My[i]), abs(Mz[i]),i))/(1.5*self.S[i])
        f.write("Ratio platine     :"+ str(round(ratio,3)))
        f.close()
        return ratio

    def ratio4chevilles(self, niveau, Fx, Fy, Fz, Mx, My, Mz,i):
        ratio = []
        print("contrainte de membrane ", self.adm_platine.cm4chevilles(Fx[i], Fy[i], Fz[i],Mx[i] , My[i] ,Mz[i],i))
        print("contrainte de flexion", self.adm_platine.flex4chevilles(Fx[i], Fy[i], Fz[i],Mx[i] , My[i] ,Mz[i],i ))
        print("contrainte max cm + cb",self.adm_platine.cm4chevilles(Fx[i], Fy[i], Fz[i],Mx[i] , My[i] ,Mz[i],i)+self.adm_platine.flex4chevilles(Fx[i], Fy[i], Fz[i],Mx[i] , My[i] ,Mz[i],i))
        if niveau == "oab":
            ratio.append(self.adm_platine.cm4chevilles(Fx[i], Fy[i], Fz[i], Mx[i], My[i], Mz[i],i)/self.SPlatine[i])
            ratio.append((self.adm_platine.cm4chevilles(Fx[i], Fy[i], Fz[i], Mx[i], My[i], Mz[i],i)+self.adm_platine.flex4chevilles(Fx[i], Fy[i], Fz[i], Mx[i], My[i], Mz[i],i))/(1.5*self.SPlatine[i]))
        elif niveau == "d":
            print("adm",[self.coefDuct[i]*min(1.5*self.SyPlatine[i],0.8*self.SuPlatine[i]),self.coefDuct[i]*min(self.SyPlatine[i],0.5*self.SuPlatine[i])] )
            ratio.append(self.adm_platine.cm4chevilles(Fx[i], Fy[i], Fz[i], Mx[i], My[i], Mz[i],i) / (self.coefDuct[i]*min(self.SyPlatine[i],0.5*self.SuPlatine[i]))) #TODO à modifier pour prendre Sy du profilé au niveau de la platine
            ratio.append((self.adm_platine.cm4chevilles(Fx[i], Fy[i], Fz[i], Mx[i], My[i], Mz[i],i) + self.adm_platine.flex4chevilles(Fx[i], Fy[i],Fz[i], Mx[i],My[i],Mz[i], i)) / (self.coefDuct[i]*min(1.5*self.SyPlatine[i],0.8*self.SuPlatine[i])))
        f = open("C:\\Users\\fitiantsoa.antenaina\\Desktop\\aster\\result.txt", "a")
        f.write("Ratio platine     :" + str(round(max(ratio), 3)))
        f.close()
        return max(ratio)


