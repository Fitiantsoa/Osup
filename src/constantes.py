import os
VERSION = "1.0"
SETTINGS_PATH = os.getcwd()
PATH = os.getcwd()
TEMP = os.getcwd() + "/src/temp/"
GMSH = os.getcwd() + "/gmsh-4.0.7-Windows64/gmsh.exe"
MED_GMSH = os.getcwd() + "/gmsh-4.0.7-Windows64/gmsh " + os.getcwd() + "/code-aster_v2019_std-win64/v2019/14.4/share/aster/tests/osup.geo -1 -format med"

MATERIAL_DB = os.getcwd() + "/databases/material.json"
PROFILE_DB = os.getcwd() + "/databases/profile(2).json"
STIRRUP_DB = os.getcwd() + "/databases/stirrup.json"
DOWEL_DB = os.getcwd() + "/databases/basededonneechevilleosup.json"
CONCRETE_DB = os.getcwd() + "/databases/concretedatabase.json"
CONCRETE_ETAG_DB = os.getcwd() + "/databases/concretedatabaseetag.json"

BEAMS_GROUP_SUFFIX = ""
NODE_GROUP_SUFFIX = ""

DICHOTOMIE_COUBE_X = os.getcwd() + "/src/temp/commCourbe_X.txt"
DICHOTOMIE_COUBE_Y = os.getcwd() + "/src/temp/commCourbe_Y.txt"
DICHOTOMIE_COUBE_Z = os.getcwd() + "/src/temp/commCourbe_Z.txt"
DICHOTOMIE_RATIO = os.getcwd()+ "/src/temp/commRatio_file.txt"
CHEVILLE_COMM = os.getcwd()+ "/src/temp/commcheville.txt"
FICHIER_CHEVILLE_RATIO = os.getcwd()+ "/src/temp/commchev_file.txt"

ASTER = os.getcwd() + "/code-aster_v2019_std-win64//v2019//bin//as_run --test osup"
ASTER_CHEVILLE = os.getcwd() + "/code-aster_v2019_std-win64//v2019//bin//as_run --test cheville"

PROFILE_RSLT = ("'" + TEMP + "profile(2).Osup" + "'").replace("\\","/")
PLATINE_RSLT = ("'" + TEMP + "platine'").replace("\\","/")
CHEVILLE_RSLT = ("'" + TEMP + "cheville(2)'").replace("\\","/")
RIGIDITE_PLAT_RSLT = ("'" + TEMP + "rigidite_plat'").replace("\\","/")
FLECHE_RSLT = ("'" + TEMP + "fleche(2).Osup" + "'").replace("\\","/")

COMM_FILE = os.getcwd() + "/code-aster_v2019_std-win64/v2019/14.4/share/aster/tests/osup.comm"
EXPORT_FILE = os.getcwd() + "/code-aster_v2019_std-win64/v2019/14.4/share/aster/tests/osup.export"
resu_PATH = os.getcwd() + "/code-aster_v2019_std-win64/v2019/14.4/share/aster/tests/osup.resu"
mess_PATH = os.getcwd() + "/code-aster_v2019_std-win64/v2019/14.4/share/aster/tests/osup.mess"
GEO_FILE = os.getcwd() + "/code-aster_v2019_std-win64/v2019/14.4/share/aster/tests/osup.geo"

COMM_FILE_DATA = os.getcwd() + "/src/temp/cheville_comm_data.txt"
COMM_FILE_CHEVILLE = os.getcwd() + "/code-aster_v2019_std-win64/v2019/14.4/share/aster/tests/cheville.comm"
EXPORT_FILE_CHEVILLE = os.getcwd() + "/code-aster_v2019_std-win64/v2019/14.4/share/aster/tests/cheville.export"

PATH_TEMPLATE_NOTE_RCCM = TEMP + "[Template]NoteDeCalcul_RCCM.docx"