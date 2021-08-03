from src.constantes import *
from src.utils import sort_beam_by, read_json
from src.modules.calculation_module import Calculation_var
from src.mocks.result_file import ResultFile

class CommFile:
    def __init__(self, data):
        self.calc_cond= data['calculation_condition']
        self.verif_mod = data['verification_module']
        self.plat_data = data['platine_data']
        self.list_liaison = self.liaison_ddl(data['geo']['node_rep'], data['geo']['beam_list'],data['verification_module']['load_node'])
        self.beam_group = data['geo']['beam_group']
        self.node_group = data['geo']['node_group']
        self.calc_var = Calculation_var( data['geo'],self.plat_data)
        self.material_database = read_json(MATERIAL_DB)
        self.section_database = read_json(PROFILE_DB)
        self.loads = []
        self.meshes = []
        self.content = []
        self.result_file = ResultFile("")

    def write(self):
        self.__read_meshes()
        self.__write_model()
        self.__create_material()
        self.__write_section()
        self.__write_limits_conditions()
        if self.verif_mod['methode'] == 'courbe':
            self.__write_dichotomy()
        else:
            self.__post_treatment()
        with open(COMM_FILE, "w", encoding='utf-8') as f:
            f.write('\n'.join(self.content))
            f.close()

    def __read_meshes(self):
        self.content.append("DEBUT(PAR_LOT='NON');")
        self.content.append("from Utilitai.Osup.constant import *")
        self.content.append("from Utilitai.OsupMAJ.ratioPlatine import RatioPlatine")
        self.content.append("from Utilitai.OsupMAJ.ratio import Ratio")
        self.content.append("import time")
        self.content.append(f"value = {self.calc_var.get_value()}")
        self.content.append(f'niveau = "{self.calc_cond["level"]}"')
        self.content.append("mesh=LIRE_MAILLAGE( INFO=2,")
        self.content.append("    UNITE=20,FORMAT='MED',);")
        self.content.append("")
        self.content.append("mesh=DEFI_GROUP(reuse =mesh,MAILLAGE=mesh,")
        self.content.append("    CREA_GROUP_MA=_F(NOM='TOUT',TOUT='OUI',),")
        self.content.append("    CREA_GROUP_NO=(_F(TOUT_GROUP_MA='OUI',),)")
        self.content.append(");")
        self.content.append("")

    def __write_model(self):
        group_id = []
        for gp in self.beam_group:
            group_id.append(gp['id'])
        self.content.append("model=AFFE_MODELE(MAILLAGE=mesh,")
        self.content.append("   AFFE=(_F(GROUP_MA=('" + "','".join(group_id) + "',),")
        self.content.append("       PHENOMENE='MECANIQUE',")
        self.content.append("       MODELISATION='POU_D_T',),")
        self.content.append("   ),")
        self.content.append(");")
        self.content.append("")

    def __create_material(self):
        list_mat = []
        gp_mat = {}

        for group in self.beam_group:
            if len(list_mat) >= 1:
                for i in range(len(list_mat)):
                    if group['material'] not in list_mat[i]:
                        list_mat.append([group['material'], group['production'], group['temperature']])
            else:
                list_mat.append([group['material'], group['production'], group['temperature']])
            if group['material'] not in gp_mat.keys():
                gp_mat[group['material']] = []

        for group in self.beam_group:
            for mat in gp_mat.keys():
                if group['material'] == mat:
                    gp_mat[mat].append(group['id'])
        for mat in list_mat:
            mat_name = mat[0].replace("≤","")
            mat_name = mat_name[0:7]
            self.content.append(str(mat_name.replace(" ",""))+"=DEFI_MATERIAU(ELAS=")
            Su = self.material_database['RCC-M 2016'][mat[1]][mat[0]][mat[2]]['Su']
            Sy = self.material_database['RCC-M 2016'][mat[1]][mat[0]][mat[2]]['Sy']
            S = self.material_database['RCC-M 2016'][mat[1]][mat[0]][mat[2]]['S']
            if mat[1] != 'RIGIDE':
                E = self.material_database['RCC-M 2016'][mat[1]][mat[0]][mat[2]]['E'] * 10 ** 3
                rho = 7.85e-09
                nu = 0.3
                self.content.append( "\t_F(E =" + str(E) + ",")
                self.content.append(f"\t\tNU = 0.3, RHO ={rho},),\n")
                print("test")
                if self.verif_mod['methode'] != 'courbe':
                    self.result_file.append_material(mat[0], E, rho, nu, Sy, Su, S)
            else:
                self.content.append("\t_F(E =" + str(self.material_database['RCC-M 2016'][mat[1]][mat[0]]['20.0']['E'] * 10 ** 3) + ",")
                self.content.append("\t\tNU = 0.3, RHO = 0 ,),\n")
                self.result_file.append_material(mat_name, E, 0, 0.3, Sy, Su, S)
            self.content.append(");\n")

        self.content.append("material=AFFE_MATERIAU(MAILLAGE=mesh,")
        self.content.append("\tAFFE=(")
        for mat in gp_mat.keys():
            mat_name = mat.replace("≤", "")
            mat_name = mat_name[0:7]
            self.content.append("\t\t_F(GROUP_MA=('" + "','".join(gp_mat[mat]) + "',), MATER =" + str(mat_name.replace(" ","")))
            self.content.append("\t\t,),")
        self.content.append("\t),")
        self.content.append(");")



    def __write_section(self):
        gp_sect = {}
        gp_or = {}
        for gp in self.beam_group:
            if gp['section'] not in gp_sect.keys():
                gp_sect[gp['section']] = []

        for gp in self.beam_group:
            for sect in gp_sect.keys():
                if gp['section'] == sect:
                    gp_sect[sect].append(gp['id'])
            if float(gp['orientation']) != 0.0:
                if gp['orientation'] not in gp_or.keys():
                    gp_or[gp['orientation']] = [gp['id']]
                else:
                    gp_or[gp['orientation']].append(gp['id'])

        self.content.append("elemcar=AFFE_CARA_ELEM(MODELE=model,")
        self.content.append("   POUTRE= (")
        for sect in gp_sect.keys():
            if sect != 'RIGIDE  ':
                sec, dim = sect.split()
            else:
                sec = "RIGIDE"
                dim = " "
            A = round(float(self.section_database[sec][dim]["aire"]),4)
            IY = round(float(self.section_database[sec][dim]["iy"])*10**4,4)
            IZ = round(float(self.section_database[sec][dim]["iz"])*10**4,4)
            AY = round(A/float(self.section_database[sec][dim]["wy"]),4)
            AZ = round(A/float(self.section_database[sec][dim]["wz"]),4)
            JX = round(float(self.section_database[sec][dim]["ig"])*10**4,4)
            Welz = float(self.section_database[sec][dim]["welz"])
            Wely = float(self.section_database[sec][dim]["wely"])
            Igr = float(self.section_database[sec][dim]["igr"])
            if sec[0] != "H":
                RY = round(IZ / ( Welz * 10**3),4)
                RZ = round(IY / ( Wely * 10**3),4)
            else:
                RZ = round(IZ/ (Welz * 10**3),4 )
                RY = round(IY / (Wely * 10**3),4)
            RT = round((JX / Igr * 10**3),4)
            self.content.append("\t\t_F(GROUP_MA=('"+ str("','".join(gp_sect[sect])) + "',),")
            self.content.append("\t\tSECTION = 'GENERALE',")
            self.content.append("\t\tCARA=('A','IY','IZ','AY','AZ','JX','RY','RZ','RT',),")
            self.content.append("\t\tVALE=({},{},{},{},{},{},{},{},{},),),".format(A,IY,IZ,AY,AZ,JX,RY,RZ,RT))
            if self.verif_mod['methode'] != 'courbe':
                self.result_file.append_section(sect.replace(" ",""),A,IY,IZ,AY,AZ,JX,Wely,Welz,Igr)
        self.content.append("\t),")
        if gp_or.keys != []:
            for orientation in gp_or.keys():
                self.content.append("\tORIENTATION=_F(")
                self.content.append("\t\tGROUP_MA = ('" + "','".join(gp_or[orientation]) + "',) ,")
                self.content.append("\t\tCARA = 'ANGL_VRIL',")
                self.content.append(f"\t\tVALE = {orientation},")
                self.content.append("\t),")
        self.content.append(");")
        self.content.append("")


    def __write_limits_conditions(self):
        self.content.append("encast=AFFE_CHAR_MECA(MODELE=model,")
        for boundary in self.node_group.keys():
            if self.node_group[boundary] != []:
                #b_name stands for boundary
                b_name = (boundary.replace("_",""))
                if len(b_name) >= 8:
                    name = b_name[:8]
                else:
                    name = b_name
                self.content.append("\tDDL_IMPO=(_F(GROUP_NO=('" + name + "',),")
                if boundary != "encas":
                    self.content.append("\t\t" + "= 0,".join(boundary.split("_"))  + " = 0,),),")
                else:
                    self.content.append("\t\t DX = 0,DY = 0, DZ = 0, DRX = 0, DRY = 0, DRZ = 0,),),")

        if self.list_liaison is not None or  self.list_liaison != []:
            self.content.append("\tLIAISON_DDL =(")
            for node_link_list in self.list_liaison:
                self.content.append("\t\t_F (NOEUD = ('N" + str(node_link_list[0]) + "', 'N" + str(node_link_list[1]) + "'),")
                self.content.append("\t\tDDL = ('DX', 'DX',),")
                self.content.append("\t\tCOEF_MULT = (1.,-1.,),")
                self.content.append("\t\tCOEF_IMPO = 0.,),")
                self.content.append("\t\t_F (NOEUD = ('N" + str(node_link_list[0]) + "', 'N" + str(node_link_list[1]) + "'),")
                self.content.append("\t\tDDL = ('DY', 'DY',),")
                self.content.append("\t\tCOEF_MULT = (1.,-1.,),")
                self.content.append("\t\tCOEF_IMPO = 0.,),")
                self.content.append("\t\t_F (NOEUD = ('N" + str(node_link_list[0]) + "', 'N" + str(node_link_list[1]) + "'),")
                self.content.append("\t\tDDL = ('DZ', 'DZ',),")
                self.content.append("\t\tCOEF_MULT = (1.,-1.,),")
                self.content.append("\t\tCOEF_IMPO = 0.,),")
                self.content.append("\t\t_F (NOEUD = ('N" + str(node_link_list[0]) + "', 'N" + str(node_link_list[1]) + "'),")
                self.content.append("\t\tDDL = ('DRX', 'DRX',),")
                self.content.append("\t\tCOEF_MULT = (1.,-1.,),")
                self.content.append("\t\tCOEF_IMPO = 0.,),")
                self.content.append("\t\t_F (NOEUD = ('N" + str(node_link_list[0]) + "', 'N" + str(node_link_list[1]) + "'),")
                self.content.append("\t\tDDL = ('DRY', 'DRY',),")
                self.content.append("\t\tCOEF_MULT = (1.,-1.,),")
                self.content.append("\t\tCOEF_IMPO = 0.,),")
                self.content.append("\t\t_F (NOEUD = ('N" + str(node_link_list[0]) + "', 'N" + str(node_link_list[1]) + "'),")
                self.content.append("\t\tDDL = ('DRZ', 'DRZ',),")
                self.content.append("\t\tCOEF_MULT = (1.,-1.,),")
                self.content.append("\t\tCOEF_IMPO = 0.,),")
            self.content.append("\t),")
        self.content.append(");")
        self.content.append("")

    def liaison_ddl(self, node_rep_list_init,beam_list,load_node):
        list_ddl_impo = []
        list_beam = list(map(lambda x: [x['n1'],x['n2']],beam_list))
        list_node = [node_rep_list_init[str(load_node)][0]]
        node_rep_max = max(list(map(lambda x:len(node_rep_list_init[x]),node_rep_list_init.keys())))
        list_ddl_node = list_node
        node_rep_list = node_rep_list_init
        while node_rep_max > 1:
            list_node = []
            for find_node in list_ddl_node:
                print()
                for beam in list_beam:
                    #parcours la liste de liste de noeuds qui forment les bares
                    if find_node in beam:
                        #cherche le noeud de charegement dans la liste précédente
                        beam.remove(find_node)
                        #il supprime ce dernier pour récupérer l'autre noeud à l'extrémité de la poutre
                        for node_base,rep_list in node_rep_list.items():
                            if beam[0] in rep_list and len(rep_list) >= 2:
                                for node_id in rep_list:
                                    if node_id != beam[0]:
                                        list_ddl_impo.append([min(node_id,beam[0]),max(node_id,beam[0])])
                                        list_node.append(node_id)
                                node_rep_list[node_base] = [node_base]
                        list_ddl_node = list_node
            node_rep_max = max(list(map(lambda x: len(node_rep_list[x]), node_rep_list.keys())))
        return list_ddl_impo

    def __write_load(self):
        fx = self.verif_mod['fx']
        fy = self.verif_mod ['fy']
        fz = self.verif_mod['fz']
        self.content.append(f"fx = {fx}")
        self.content.append(f"fy = {fy}")
        self.content.append(f"fz = {fz}")
        osup_file = open(DICHOTOMIE_RATIO, 'r')
        lines = osup_file.readlines()
        for line in lines:
            if "***********load*********" in line:
                line.replace("***********load*********", f'FX = fx, FY = fy, FZ = fz')
            self.content.append(line)



    def __write_dichotomy(self):
        #TODO enlever friction load de verif_mod
        self.content.append(f'curveFile = {PROFILE_RSLT}')
        self.content.append(f'platineFile = {PLATINE_RSLT}')
        self.content.append(f'chevilleFile = {CHEVILLE_RSLT}')
        if self.verif_mod["axis"] == 'X' or self.verif_mod["axis"] =='':
            osup_file = open(DICHOTOMIE_COUBE_X, 'r')
        elif self.verif_mod["axis"] == 'Y':
            osup_file = open(DICHOTOMIE_COUBE_Y, 'r')
        else:
            osup_file = open(DICHOTOMIE_COUBE_Z, 'r')

        lines = osup_file.readlines()
        if self.calc_cond["friction_coefficient"] != "":
            self.content.append(f'f = {self.calc_cond["friction_coefficient"]}')
        else:
            self.content.append(f'f = 0.3')
        if self.verif_mod["points"] != "":
            self.content.append(f'n = {self.verif_mod["points"]}')
        else:
            self.content.append('n = 10')
        if self.calc_cond["ratio_profile"] != "":
            self.content.append(f'ratioLimProf = {self.calc_cond["ratio_profile"]}')
        else:
            self.content.append(f'ratioLimProf = 1')
        if self.calc_cond["ratio_platine"] != "":
            self.content.append(f'ratioLimPlat = {self.calc_cond["ratio_platine"]}')
        else:
            self.content.append(f'ratioLimPlat = 1')
        for line in lines:
            self.content.append(line)

    def __post_treatment(self):
        fx = self.verif_mod['fx']
        if self.verif_mod['fy'] != "":
            fy = self.verif_mod['fy']
        else:
            fy = 0
        if self.verif_mod['fz'] != "":
            fz = self.verif_mod['fz']
        else:
            fz = 0
        osup_file = open(DICHOTOMIE_RATIO, 'r')
        lines = osup_file.readlines()
        rslt_file = self.verif_mod['folder_path'] + "/result.osup"
        for line in lines:
            if "***********load*********" in line:
                line = ""
                if fx != "":
                    line += f'\tFX = {fx},'
                if fy != "":
                    line += f'FY = {fy},'
                if fz != "":
                    line += f'FZ = {fz},'
                line += "),"
            if "*************result_file*********" in line:
                line = f"result_file = '{rslt_file}'"
            self.content.append(line)
        self.content.append(f"result_file = '{rslt_file}'")
        self.result_file.write_load(fx, fy, fz, self.calc_cond["level"])
        self.result_file.create_result_file(rslt_file) #On écrit qu'un seul chargement par fichier



    def open(self):
        try:
            os.startfile(COMM_FILE)
            return True
        except:
            print(sys.exc_info())
            return False

    def new_file(self):
        new_comm = open(COMM_FILE, "w")
        new_comm.close()