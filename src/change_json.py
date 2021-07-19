
from src.constantes import *
from src.utils import sort_beam_by, read_json

if __name__ == "__main__":
    jsonfile = read_json("C:\\Users\\fitiantsoa.antenaina\\Desktop\\Developpement\\OSup\\databases\\profile.json")
    newjson = open("C:\\Users\\fitiantsoa.antenaina\\Desktop\\newjson.json","w")
    newjson.write("{")
    for key in jsonfile.keys():
        newjson.write(f"{key} :")
        for data in jsonfile[key].keys():
            newjson.write(f"{data} :")
            newjson.write(str(jsonfile[key][data]))
            newjson.write(", ")
        newjson.write("}, ")
    newjson.close()
