import os
import sys
from src.constantes import *


class ExportFile:
    #PATH = TEMP + "osup.export"

    def write(self, filetype):
        content = []
        fresu = open(resu_PATH, "w")
        fresu.close()
        fmess = open(mess_PATH, "w")
        fmess.close()
        content.append("P time_limit 6000")
        content.append("P memory_limit 6000")
        content.append("P ncpus 1")
        content.append("P mpi_nbcpu 1")
        content.append("P mpi_nbnoeud 1")
        content.append("P testlist verification sequential")
        content.append("F comm " + filetype + ".comm D 1")
        content.append("F med osup.med D 20")
        content.append("F mess osup.mess R 6")
        content.append("F resu osup.resu R 8")

        if filetype == "osup":
            export_file = EXPORT_FILE
        else:
            export_file = EXPORT_FILE_CHEVILLE

        with open(export_file, "w", encoding='utf-8') as f:
            f.write('\n'.join(content))
            f.close()

    def open(self):
        try:
            os.startfile(EXPORT_FILE)
            return True
        except:
            print(sys.exc_info())
            return False