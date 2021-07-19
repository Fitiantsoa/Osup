

class ResultRatio():

    def getStressValue(self):
        resultFile = os.environ["HOMEPATH"] + "\\Desktop\\aster\\fort.8"
        fresult = open(resultFile,"r")
        data = {"Sn" : [], "Svy" : [], "Svz" : [],"Smt" : [], "Smfy" : [], "Smfz" : [],"node" :[]}
        line = fresult.readline()
        while line.find("Contrainte")>1:
            value = line.split()
            data["node"].append(value[1])
            data["Sn"].append(value[10])
            data["Svy"].append(value[11])
            data["Svz"].append(value[12])
            data["Smt"].append(value[13])
            data["Smfy"].append(value[14])
            data["Smfz"].append(value[15])
            line = fresult.readline()
        return data

