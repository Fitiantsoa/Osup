import sys, os, json, shutil, subprocess
from PyQt5.QtCore import *
from src.constantes import *
# from src.components.admin_module import AdminMenu
from src.modules.db_module import DbMenu
from src.modules.calculation_condition import CalculationCondition
from src.modules.module_verif import ModuleVerif
from src.modules.modulePlatine import ModulePlatine
from src.modules.calculation_module import Calculation_var
from src.modules.geometry import Geometry
from src.modules.stirrup import Stirrup
from src.modules.results_window import ResultWindow
from src.mocks.geo_file import GeoFile
from src.mocks.comm_file import CommFile
from src.mocks.export_file import ExportFile
from src.mocks.result_file import ResultFile
from src.modules.module_extract_note import NoteDeCalcul
from src.Version5etag.general import General

path = str(sys.path[0])


class OSup(QObject):
    def __init__(self, parent, console, app):
        super().__init__()
        self.version = VERSION
        self.parent = parent
        self.app = app
        # Saving
        self.file_name = None
        self.saved = True
        self.force_new = False
        # Files
        self.geo_file = None
        self.med_file = None
        self.export_file = None
        self.comm_file = None
        self.result_file = None
        # Admin
        # self.adminMenu = AdminMenu(parent)
        self.db_menu = DbMenu(parent)
        # self.console = console
        # sys.excepthook = self.unhandled_exception
        # Modules
        self.calculation_condition = CalculationCondition(parent)
        self.geometry_module = Geometry(parent)
        self.verification_module = ModuleVerif(parent)
        self.platine_data = ModulePlatine(parent)
        self.stirrup_module = Stirrup(parent)
        self.result_window = None
        self.need_to_be_saved_init()
        self.data = {}
        self.data_stirrup = {}
        self.create_result_file()
        self.created_file = False
        self.note = NoteDeCalcul(parent, app)

    def unhandled_exception(self, ex_cls, ex, tb):
        import traceback
        with open("log.txt", "w") as f:
            f.write(''.join(traceback.format_tb(tb)), file=sys.stderr)
            f.write('{0}: {1}'.format(ex_cls, ex), file=sys.stderr)
        # self.parent.findChild(QObject, "unHandledException").open()
        # self.save_to_file_as("sauv.osup")

    @pyqtSlot(result=str)
    def get_version(self):
        return "OSUP version " + self.version

    @pyqtSlot(result=bool)
    def get_saved_state(self):
        return self.saved

    @pyqtSlot()
    def write_recent_file(self):
        recent_file = []
        if self.file_name is not None and self.file_name != "":
            try:
                with open(SETTINGS_PATH + "\\recentFile.txt", "r") as f:
                    recent_file = json.loads(f.read())
                    if len(recent_file) >= 5:
                        if self.file_name not in recent_file:
                            del recent_file[0]
                        else:
                            del recent_file[recent_file.index(self.file_name)]
                    else:
                        if self.file_name in recent_file:
                            del recent_file[recent_file.index(self.file_name)]
                    recent_file.append(self.file_name)
            except:
                recent_file.append(self.file_name)
                print("ERREUR : Aucun fichier recent", file=sys.stderr)

            with open(SETTINGS_PATH + "\\recentFile.txt", "w") as f:
                f.write(json.dumps(recent_file))
            return True

    def get_saved_data(self):
        return {
            "calculation_condition": self.calculation_condition.get_data(),
            "verification_module": self.verification_module.get_data(),
            "platine_data" : self.platine_data.get_data(self.geometry_module.get_models()),
            "geo": self.geometry_module.get_models(),
            "stirrup": self.stirrup_module.get_data(),
            "cheville": General(self.platine_data.get_dowel_data()).input_data_aster(),
            "input_data_dowel": self.platine_data.get_dowel_data()

             }

    def update_from_file(self, data):
        self.calculation_condition.update_from_file(data['calculation_condition'])
        self.geometry_module.update_from_file(data['geo'])
        self.platine_data.update_from_file(data['platine_data'], data['input_data_dowel'])
        self.stirrup_module.update_from_file(data['stirrup'])
        self.verification_module.update_from_file(data['verification_module'])

    @pyqtSlot(str)
    def save_to_file_as(self, file_name):
        self.file_name = file_name.lstrip("file:///")
        print("saved data", self.get_saved_data()['cheville'])
        try:
            with open(self.file_name, "w") as fic:
                fic.write(json.dumps([self.version, self.get_saved_data()]))
                print("Fichier Osup enregistré")
        except:
            print("ERREUR : Impossible de sauvegarder le fichier .osup", file=sys.stderr)
            print(sys.exc_info())

        self.saved = True
        self.parent.setProperty("title", "Osup - Version Beta " + self.file_name)
        if self.force_new:
            self.force_new_file()
            self.force_new = False

    @pyqtSlot()
    def save_to_file(self):
        if self.file_name is not None:
            self.save_to_file_as(self.file_name)
            self.write_recent_file()
        else:
            self.parent.findChild(QObject, "saveAsDialog").open()

    @pyqtSlot(str)
    def read_from_file(self, file_name):
        self.file_name = file_name.lstrip("file:///")

        with open(self.file_name, "r") as f:
            try:
                self.update_from_file(json.loads(f.read())[1])
            except:
                print("ERREUR : Impossible de lire le fichier .osup", file=sys.stderr)
                print(sys.exc_info())

        self.parent.setProperty("title", "Osup - " + self.version + " " + self.file_name)
        self.app.processEvents()
        self.saved = True

    @pyqtSlot()
    def new_file(self):
        if not self.saved:
            self.parent.findChild(QObject, "workNotSaved").open()
        else:
            self.force_new_file()

    @pyqtSlot()
    def save_before_close(self):
        self.save_to_file()

    @pyqtSlot()
    def save_before_new_file(self):
        self.force_new = True
        self.save_to_file()

    @pyqtSlot()
    def force_new_file(self):
        self.geometry_module.new_file()
        self.platine_data.new_file()
        self.verification_module.new_file()
        self.saved = True
        self.parent.setProperty("title", "OSup - " + self.version)
        self.file_name = None
        try:
            self.geo_file.new_file()
            self.comm_file.new_file()
        except:
            f_geo = open(GEO_FILE, "w")
            f_geo.close()
            f_comm = open(COMM_FILE, "w")
            f_comm.close()


    @pyqtSlot()
    def need_to_be_saved(self):
        self.saved = False
        # print("need to be saved")

    def need_to_be_saved_init(self):
        self.geometry_module.node_list_view._sibling.property("model").dataChanged.connect(self.need_to_be_saved)
        self.geometry_module.beam_list_view._sibling.property("model").dataChanged.connect(self.need_to_be_saved)

    @pyqtSlot()
    def open_console(self):
        if self.console is not None:
            self.console.show()

    @pyqtSlot()
    def close_console(self):
        if self.console is not None:
            self.console.close()

    @pyqtSlot(QObject)
    def init_data_manager(self, window):
        self.db_menu.parent = window
        self.db_menu.materiaux.parent = self.db_menu.sections.parent = window

    @pyqtSlot(result=bool)
    def beam_list_empty(self):
        self.geometry_module.get_models()
        self.geometry_module.get_node_list()
        self.geometry_module.get_beam_group()
        self.geometry_module.get_node_group()
        if self.geometry_module.get_models()["beam_list"] == []:
            return True
        else:
            return False

    @pyqtSlot(int,int,str,str,result=str)
    def printImage(self, n1, n2, section,orientation):
        return self.geometry_module.printImage(n1, n2, section,orientation)

    @pyqtSlot(int, result=str)
    def printPipeimage(self,node):
        node_or_dict = self.geometry_module.pipe_orientation()
        if node_or_dict != {}:
            print(node_or_dict[str(node)])
            return node_or_dict[str(node)]
        else:
            return None

    @pyqtSlot(result=bool)
    def check_list(self):
        if self.geometry_module.get_models()['node_group']['encas'] != []:
            return True
        else:
            return False

    @pyqtSlot(result=bool)
    def check_free_node(self):
        if self.geometry_module.check_free_node():
            return True
        else:
            return False
    @pyqtSlot()
    def reinitialize_value(self):
        self.data = {}
        self.platine_data.reinitialize_platine()

    @staticmethod
    @pyqtSlot(list, result=bool)
    def empty_list(list):
        if list != []:
            return True

    @pyqtSlot(result=bool)
    def check_node_load(self):
        load_node = self.verification_module.get_data()['load_node']
        nodes = self.geometry_module.get_models()['node_init']
        find = False
        for node in nodes:
            print("node id", [node['id'],load_node,node['ap']])
            if node['id'] == int(load_node) and node['ap'] == 'Encastrement':
                find = True
        return find

    @pyqtSlot(result=bool)
    def check_pipe_axis(self):
        try:
            pipe_axis = self.verification_module.get_data()['axis']
            if self.verification_module.get_data()['methode'] == "courbe":
                if pipe_axis == "":
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    @pyqtSlot()
    def update_widget(self):
        self.app.processEvents(QEventLoop.ExcludeUserInputEvents)


    @pyqtSlot(str, result=bool)
    def create_file(self, file_type):
        if self.data == {}:
            self.data = self.get_saved_data()
        if file_type == "geo":            #on ne crée les groupes qu'une seule fois sinon existence doublon
            self.geo_file = GeoFile(self.data)
            self.geo_file.write()
            return True

        elif file_type == "med":
            os.system(MED_GMSH)
            return True

        elif file_type == "comm":
            self.comm_file = CommFile(self.data)
            self.comm_file.write()
            return True

        elif file_type == "export":
            self.export_file = ExportFile()
            self.export_file.write()
            self.created_file = True
            return True

    def create_result_file(self):
        resultfile = os.environ["HOMEPATH"] + "\\Desktop\\aster"
        if not os.path.exists(resultfile):
            os.makedirs(resultfile)

    @pyqtSlot(str)
    def open_file(self, file_type):
        # if self.geo_file is None:
        #     self.create_file(file_type)

        if file_type == "geo":
            return self.geo_file.open()

        if file_type == "med":
            return self.med_file.open()

        if file_type == "export":
            return self.export_file.open()

        if file_type == "comm":
            return self.comm_file.open()

    @pyqtSlot()
    def open_file_gmsh(self):
        #gmsh = shutil.which('gmsh.exe')
        if self.geo_file is None:
            self.create_file("geo")
        subprocess.Popen([GMSH, GEO_FILE])


    @pyqtSlot()
    def run_aster(self):
        self.run_calculation()
        self.display_result()

    def run_calculation(self):
        os.system(ASTER)

    @pyqtSlot(str)
    def import_curve(self, file_name):
        filename = file_name.lstrip("file:///")
        title, axis = self.write_in_File(filename)
        self.result_window = ResultWindow(axis,filename,title)
        self.result_window.import_from_file(filename)
        self.result_window.showMaximized()

    @staticmethod
    def write_in_File(filepath):
        f = open(filepath, "r")
        plat_file = open(PLATINE_RSLT.replace("'", ""), "w")
        prof_file = open(PROFILE_RSLT.replace("'", ""), "w")
        lines = f.readlines()
        for line in lines:
            data = line.split()
            if "Titre:" in data:
                title = data[1]
            elif "Axe:" in data:
                axis = data[1]
            elif data[0] == "PR" and len(data) > 1:
                prof_file.write(" ".join(data[1:]))
                prof_file.write("\n")
            elif data[0] == "PL" and len(data) > 1:
                plat_file.write(" ".join(data[1:]))
                plat_file.write("\n")
        plat_file.close()
        prof_file.close()
        return title, axis

    @pyqtSlot(str)
    def display_result(self, result_file=None):
        if "axis" in self.get_saved_data()["verification_module"].keys() :
            pipe_axis = self.get_saved_data()["verification_module"]["axis"]
            self.result_file = ResultFile(pipe_axis)
            self.result_file.load(result_file,"profile")
            nb_point = self.get_saved_data()["verification_module"]['points']
            self.result_window = ResultWindow(pipe_axis)
            self.result_window.load_result(self.result_file.get_plot_data(),"Profilé")
            self.result_file.load(result_file, "platine")
            self.result_window.load_result(self.result_file.get_plot_data(), "Platine")
            self.result_file.load(result_file, "cheville")
            self.result_window.load_result(self.result_file.get_plot_data(), "Cheville")
            if self.data_stirrup == {}:
                self.result_window.load_result(self.result_file.get_dict_data(self.get_saved_data()["verification_module"]['points'],self.get_saved_data()["stirrup"]["plot_data"]), "Etrier")
            else:
                self.result_window.load_result(self.result_file.get_dict_data(self.get_saved_data()["verification_module"]['points'],self.data_stirrup), "Etrier")
            self.result_window.showMaximized()


        else:
            try:
                resultFile = "C:" + os.environ["HOMEPATH"] + "/Desktop/aster/result.osup"
                os.startfile(resultFile)
                return True
            except:
                print(sys.exc_info())
                return False

    @pyqtSlot(str, str)
    def update_stirrup_thickness(self, beam_id, thickness):
        self.parent.findChild(QObject, "tTF").setProperty('text', self.geometry_module.get_beam_thickness(beam_id, thickness))

    @pyqtSlot(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    def append_stirrup(self, name, mat, Sb, As, d, L, t, pas, Sy, fy, Su, fu, Fub, A, dm, do, tp, pCisaill, fraise, p1u, e1u, e2u):
        norm = self.calculation_condition.get_norm()
        level = self.calculation_condition.get_level()
        if self.calculation_condition.get_data()["friction_coefficient"] == "":
            coeff = 0.3
        else:
            coeff = float(self.calculation_condition.get_data()["friction_coefficient"])

        cEtrier = self.stirrup_module.append(norm, level, coeff, name, mat, Sb, As, d, L, t, pas, Sy, fy, Su, fu, Fub,
                                             A, dm, do, tp, pCisaill, fraise, p1u, e1u, e2u)
        self.data_stirrup = cEtrier.plots
        self.stirrup_module.get_plot_data(self.data_stirrup)


    @pyqtSlot(str)
    def remove_stirrup(self, name):
        #TODO modifier pour prendre en compte les modif result window
        try:
            self.result_window.remove_plot(name)
        except:
            del self.get_saved_data()["stirrup"]["plot_data"][name]

    @pyqtSlot()
    def extractNote(self):
        self.note.generateNote()

    @pyqtSlot(str)
    @pyqtSlot(int)
    @pyqtSlot(bool)
    @pyqtSlot(list)
    @pyqtSlot(QModelIndex)
    @pyqtSlot(QVariant)
    def print(self, text):
        print(text)


