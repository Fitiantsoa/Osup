import os
import sys
from src.constantes import *


class ExportFile:
    #PATH = TEMP + "osup.export"

    def __init__(self):
        self.content = []

    def write(self):
        fresu = open(resu_PATH, "w")
        fresu.close()
        fmess = open(mess_PATH, "w")
        fmess.close()
        self.content.append("P time_limit 6000")
        self.content.append("P memory_limit 6000")
        self.content.append("P ncpus 1")
        self.content.append("P mpi_nbcpu 1")
        self.content.append("P mpi_nbnoeud 1")
        self.content.append("P testlist verification sequential")
        self.content.append("F comm osup.comm D 1")
        self.content.append("F med osup.med D 20")
        self.content.append("F mess osup.mess R 6")
        self.content.append("F resu osup.resu R 8")

        try:
            with open(EXPORT_FILE, "w", encoding='utf-8') as f:
                f.write('\n'.join(self.content))
                f.close()
        except:
            f =open(EXPORT_FILE, "w")
            f.write('\n'.join(self.content))
            f.close()


    def open(self):
        try:
            os.startfile(EXPORT_FILE)
            return True
        except:
            print(sys.exc_info())
            return False