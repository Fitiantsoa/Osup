from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QGroupBox, QGridLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from src.utils import lerp
from src.modules.plots_data import Data
from src.modules.rw_graph import Graph
from src.modules.rw_treelist_view import TreeListView
from src.modules.rw_result_table import TableView
from src.modules.rw_export_result import ExportResult
from src.constantes import *
from src.modules.rw_data_view import DataView
from src.modules.rw_torsor_view import TorsorView
from src.modules.rw_error import Error
from tkinter import *
from tkinter import messagebox
from src.Version5etag.general import General


class ResultWindow(QWidget):

    def __init__(self, pipe_axis, filename=None, title=None):
        super().__init__()
        # UI
        if not filename:
            self.title = "Affichage des résultats Osup"
        else:
            self.title = filename
        if not title:
            self.graph_title = "Graphique"
        else:
            self.graph_title = title
        self.setMouseTracking(True)
        self.status = None
        self.horizontal_group_box = None
        self.chevilleerror = None

        # Data
        self.data = Data()
        self.pipe_axis = pipe_axis

        # Views
        self.graph = Graph(self.data, pipe_axis)
        self.tree_view = TreeListView()
        self.result_table_view_prof = TableView("profile")
        self.result_table_view_plat = TableView("platine")
        self.result_table_view_chev = TableView("cheville")
        self.export_data = ExportResult()
        self.torsor_view = TorsorView(self.data, pipe_axis)
        # self.data_view = DataView()  # TODO: Maybe we don't need it, check that with the result file values

        # Button
        self.hide_torsor = None
        self.export_img = None
        self.export_result = None

        # Errors
        self.errors = Error()
        self.init_ui()
        self.init_events()
        self.curve_data = []

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowFlags(Qt.WindowFullscreenButtonHint)
        self.create_menu_bar()
        self.create_grid_layout()
        window_layout = QVBoxLayout()
        window_layout.setMenuBar(self.status)
        window_layout.addWidget(self.horizontal_group_box)
        self.setLayout(window_layout)
        color = self.palette()
        color.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(color)
        self.setMinimumHeight(500)
        self.setMinimumWidth(900)

    def init_events(self):
        self.tree_view.toggle.connect(self.switch_plot)
        self.torsor_view.add_button.clicked.connect(self.torsor_buttons_clicked)
        self.torsor_view.remove_button.clicked.connect(self.torsor_buttons_clicked)
        self.export_data.export_button.clicked.connect(self.export_buttons_clicked)

    def clear(self):
        self.graph.clear()
        self.hide_torsor.setText("Cacher les torseurs")

    # UI
    def create_tree_view(self):
        self.tree_view.add_model()

    def create_menu_bar(self):
        self.status = QToolBar(self)

        self.export_img = QAction("Exporter image", self.status)
        self.export_img.triggered.connect(self.exportEvent)
        self.status.addAction(self.export_img)

        # self.export_result = QAction("Importer résultats", self.status)
        # self.export_result.triggered.connect(self.importResult)
        # self.status.addAction(self.export_result)

        self.hide_torsor = QAction("Cacher les torseurs", self.status)
        self.hide_torsor.triggered.connect(self.hide_torsorEvent)
        self.status.addAction(self.hide_torsor)

    def create_grid_layout(self):
        self.horizontal_group_box = QGroupBox(self.graph_title)
        layout = QGridLayout()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 0)
        layout.addWidget(self.graph.plot_widget, 0, 0, 9, 1)
        layout.addWidget(self.tree_view, 0, 1)
        title = QLabel()
        title.setText("Courbe profilé")
        layout.addWidget(title, 1, 1)
        layout.addWidget(self.result_table_view_prof, 2, 1)
        title = QLabel()
        title.setText("Courbe platine")
        layout.addWidget(title, 3, 1)
        layout.addWidget(self.result_table_view_plat, 4, 1)
        title = QLabel()
        title.setText("Courbe cheville")
        layout.addWidget(title, 5, 1)
        layout.addWidget(self.result_table_view_chev, 6, 1)
        layout.addWidget(self.export_data, 7, 1)
        layout.addWidget(self.torsor_view, 8, 1)
        # layout.addWidget(self.data_view, 2, 1)
        self.horizontal_group_box.setLayout(layout)

    # Data
    def remove_torsor(self):
        self.graph.remove_torsor()
        for plot in self.data.torsors:
            self.graph.add_torsor(plot[1], plot[2], True, False)
        self.graph.update()

    def switch_plot(self, QMouseEvent):
        tree_item = self.tree_view.toggle_plot_visible(QMouseEvent)
        if tree_item is not None:
            data, name, parent, color, check_state = tree_item
            if data is not None and check_state == 2:
                self.graph.add_plot(data["DataX"], data["DataY"], int(color), parent + " : " + name)
                self.curve_data.append(data)
            else:
                self.graph.remove_plot(name, parent)
            self.remove_torsor()
        return

    def add_torsor(self, Fy, Fz, name, status, add_to_list=True):
        if status:
            torsor_id = self.data.get_torsor_position(name)
            if torsor_id is None and name != "" or add_to_list is False:
                index = self.whatColor(float(Fy), float(Fz))
                try:
                    self.graph.add_torsor([float(Fy)], [float(Fz)], "  " + name + " ", index)
                    if add_to_list:
                        self.data.add_torsor(Fy, Fz, name)
                except:
                    self.errors.show_error("Efforts non valide")
            elif name == "":
                self.errors.show_error("Nom invalide")
            else:
                self.errors.show_error("Torseur déjà existant")
        else:
            err = True
            if self.data.remove_torsor(name):
                self.remove_torsor()
                err = False
            if err:
                self.errors.show_error("Torseur inexistant")

    def whatColor(self, Fy, Fz):
        index = 0
        curves = self.graph.plot_widget.getPlotItem().curves
        curves_data = [curve.getData() for curve in curves]
        for j, curve in enumerate(curves_data):
            if j > 2:  # Nombre à changer si de nouveaux groupes de torseurs sont ajoutés
                for i, elt in enumerate(curve[0]):
                    try:
                        if abs(elt) < abs(Fy) < abs(curve[0][i + 1]):
                            curveFz = lerp(abs(curve[1][i]), abs(curve[1][i + 1]), abs(elt), abs(curve[0][i - 1]),
                                           abs(Fy))
                            if curveFz < abs(Fz):
                                index += 1
                        elif abs(Fy) == abs(elt):
                            if abs(curve[1][i]) < abs(Fz):
                                index += 1
                    except:
                        if Fy == elt:
                            if abs(curve[1][i]) < abs(Fz):
                                index += 1
                        continue
        return index

    # Events
    def closeEvent(self, QCloseEvent):
        self.hide()
        self.graph.view_box.hide_label()

    def resizeEvent(self, QResizeEvent):
        self.graph.view_box.hide_label()
        self.graph.view_box.update_text_item()

    def exportEvent(self):
        file = self.graph.export()
        QWidget.grab(self).save(file[0], 'jpg')

    def import_from_file(self, file_path):
        frslt = file_path.split(".")[0] + "." + file_path.split(".")[1] + ".rslt"
        f = open(frslt, "r")
        lines = f.readlines()
        j = 0
        for line in lines:
            j += 1
            data = line.split()
            curve_data = []
            data_y_id = data.index("'DataY':")
            for i in range(len(data)):
                if "DataX':" in data[i] or "DataY':" in data[i]:
                    curve_data.append("data")
                else:
                    try:
                        curve_data.append(float(
                            ((((data[i].replace(",", "")).replace("[", "")).replace("]", "")).replace("{", "")).replace(
                                "}", "")))
                    except:
                        print("erreur data", data[i])
            print(curve_data)
            if j == 1:
                prof_data = {'DataX': curve_data[1:data_y_id], 'DataY': curve_data[data_y_id + 1:]}
                self.load_result(prof_data, "Profilé")
                # data["Profilé"]={"all": line}
            elif j == 2:
                plat_data = {'DataX': curve_data[1:data_y_id], 'DataY': curve_data[data_y_id + 1:]}
                self.load_result(plat_data, "Platine")
                # data["Platine"]={"all": line}
            elif j == 3:
                etr_data = {'DataX': curve_data[1:data_y_id], 'DataY': curve_data[data_y_id + 1:]}
                self.load_result(etr_data, "Etriers")
                # data["Chevilles"] = {"all":line}
            else:
                chev_data = {'DataX': curve_data[1:data_y_id], 'DataY': curve_data[data_y_id + 1:]}
                self.load_result(chev_data, "Cheville")
                # data["Chevilles"] = {"all":line}

    def exportResult(self):
        # fname = "C:" + os.environ["HOMEPATH"] + "\\Desktop\\aster\\" + file_name + ".osup"
        fname = self.export_data.export()
        cp_file = open(fname[0], "w")
        cp_file.write("Titre: " + self.export_data.get_data())
        cp_file.write("\n")
        cp_file.write("Axe: " + self.pipe_axis)
        cp_file.write("\n")
        cp_file.write("PROFILE")
        cp_file.write("\n")
        cp_file.close()
        self.copyFile(PROFILE_RSLT.replace("'", ""), fname[0], "PR")
        cp_file = open(fname[0], "a")
        cp_file.write("PLATINE")
        cp_file.write("\n")
        cp_file.close()
        self.copyFile(PLATINE_RSLT.replace("'", ""), fname[0], "PL")
        cp_file = open(fname[0], "a")
        cp_file.write("CHEVILLE")
        cp_file.write("\n")
        cp_file.close()
        self.copyFile(CHEVILLE_RSLT.replace("'", ""), fname[0], "CH")
        frslt_data = fname[0].split(".")[0] + "." + fname[0].split(".")[1] + ".rslt"
        frslt = open(frslt_data, "w")

        for data in self.curve_data:
            frslt.write(str(data))
            frslt.write("\n")
        frslt.close()

    @staticmethod
    def copyFile(result_file, fpath, comp):
        f = open(result_file, "r")
        cp_file = open(fpath, "a")
        lines = f.readlines()
        for line in lines:
            if "-------" in line:
                pass
            else:
                cp_file.write(comp + " " + line)
        f.close()
        cp_file.close()

    def hide_torsorEvent(self):
        if self.graph.torsor_visible:
            self.graph.hide_torsor_items()
            self.hide_torsor.setText("Afficher les torseurs")
        else:
            self.graph.display_torsor_items()
            self.hide_torsor.setText("Cacher les torseurs")

    def torsor_buttons_clicked(self):
        if self.chevilleerror is True:
            General(self.platine_data.get_dowel_data())
        Fy, Fz, name, status = self.torsor_view.get_data()
        self.add_torsor(Fy, Fz, name, status)

    def export_buttons_clicked(self):
        self.exportResult()

    def new_file(self):
        self.graph.new_file()

    def load_result(self, data, part):
        self.data.load_plots(data, part)
        self.tree_view.add_model(self.data.plots)

    def add_plot(self, data, key):
        self.data.add_plot(data, key)

    def affichage_message_erreur_cheville(self):
        self.message_erreur_cheville()

    def message_erreur_cheville(self):
        # fenetre = Tk()
        # fenetre.title("Erreur")
        # #  fenetre.iconbitmap("logo.ico")
        # fenetre.config(bg="#fff")
        # fenetre.geometry("440x180")
        # texte1 = Label(fenetre, text="Le calcul de chevilles d'ancrages n'a pas aboutie")
        # texte1.pack()
        # texte1.place(x=90, y=60)
        # # Création d'un cadre dans la fenêtre :
        # cadre1 = Frame(fenetre)
        # cadre1.pack()
        # cadre1.place(x=390, y=130)
        # # Ajout de boutons dans le cadre :
        # bouton1 = Button(cadre1, text="OK", command=fenetre.destroy)
        # bouton1.pack(pady = 10)
        # fenetre.mainloop()
        messagebox.showwarning("Avertissement", "Le calcul d'ancrage n'a pas aboutie")
        return self.chevilleerror is True
