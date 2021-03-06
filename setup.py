#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3

"""
Icone sous Windows: il faut:
=> un xxx.ico pour integration dans le exe, avec "icon=xxx.ico"
=> un xxx.png pour integration avec PyQt4 + demander la recopie avec includefiles.
"""

import sys
from cx_Freeze import setup, Executable

#############################################################################
# preparation des options

# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path
# options d'inclusion/exclusion des modules
includes = []  # nommer les modules non trouves par cx_freeze
excludes = []
packages = ["pyqtgraph"]  # nommer les packages utilises
# copier les fichiers non-Python et/ou repertoires et leur contenu:
includefiles = ["./src","./qml","./gmsh-4.0.7-Windows64","./code-aster_v2019_std-win64", "./assets","./databases"]

if sys.platform == "win32":
     # includefiles += ['C:\\Windows\\System32\\ucrtbase.dll'] #: ajouter les recopies specifiques à Windows
    pass
elif sys.platform == "linux2":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Linux
else:
    pass
    # includefiles += [...] : cas du Mac OSX non traite ici

# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]
# niveau d'optimisation pour la compilation en bytecodes
optimize = 0
# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
            "optimize": optimize,
           }
# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True

#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # pour application graphique sous Windows
    # base = "Console" # pour application en console sous Windows

icone = r"./osup.ico"


cible_1 = Executable(
    script="osup.py",
    base=base,
    icon=icone
)



#############################################################################
# creation du setup
setup(
    name="Osup",
    version="1.00",
    description="Osup",
    author="SOM Calcul Marseille",
    options={"build_exe": options},
    executables=[cible_1]
)