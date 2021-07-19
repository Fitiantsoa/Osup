import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import QtQuick.Dialogs 1.1

import "../theme.js" as Theme
import "../base"
import "../ui"
import "../components"

Rectangle {
    id: container
    width: parent.width
    height: title.height+corps.height
    color:"transparent"
    Rectangle {
        id:title
        width: 792
        height:  25
        color: "transparent"
        anchors.top: parent.top
        anchors.topMargin: 60
        MouseArea {
            id: mouseArea
            anchors.fill: parent
            onClicked: {
                if (corps.state == "expanded")
                    corps.state = "closed"
                else
                    corps.state = "expanded"
            }
        }
        Row{
            anchors.fill: parent
            anchors.verticalCenter: parent.verticalCenter
            Label {
                id: indicateur
                width: 20
                color: Theme.grey_6
                text: "\uE815"
                font.family: "fontello"
                anchors.verticalCenter: parent.verticalCenter
            }
            Label{
                id:moduletitle
                text:"Etape 6 : Génération des scripts"
                z:1
                color:Theme.grey_6
                font.pixelSize: Theme.text
                font.bold:true
                anchors.verticalCenter: parent.verticalCenter
            }
        }

    }
    Rectangle{
        id: corps
        color : "transparent"
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.top: title.bottom
        anchors.topMargin: 10
        state:"expanded"
        states: [
            State {
                name: "expanded"
                PropertyChanges { target: corps; height: 220}
                PropertyChanges { target: indicateur; text: "\uE815" }
            },
            State {
                name: "closed"
                PropertyChanges { target: corps; height: 0;opacity:0;visible:false}
                PropertyChanges { target: indicateur; text: "\uE818" }

            }
        ]
        transitions: [
            Transition {
                NumberAnimation {duration: 200;properties: "height"}
                NumberAnimation {duration: 200;properties: "opacity"}
                NumberAnimation {duration: 200;properties: "visible"}
            }
        ]

        //MODULE VIDE : INSERER LE CODE CI-DESSOUS
        //--------------------------------------------------------------------------------------
        Rectangle{
            border.color: Theme.grey_2
            border.width: 1
            radius: 4
            anchors.right: parent.right
            anchors.rightMargin: 60
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.top : parent.top
            anchors.bottom: parent.bottom
            Column{
                spacing : 0
                anchors.fill: parent
                anchors.margins: 10
                Row {
                    width: parent.width
                    height: 50
                    Rectangle {
                        height: parent.height
                        width: parent.width - 320
                        color: "transparent"
                        Label {
                            font.pixelSize: Theme.text
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "-  Fichier de géométrie <b>.geo</b> (permet de vérifier la géométrie avec le logiciel gmsh)"
                            anchors.leftMargin: 10

                        }
                    }
                    Rectangle {
                        height: parent.height
                        width: 75
                        color: "transparent"
                        ButtonText {
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Générer"
                            width: 65
                            onClicked:{
                                if (osup.check_free_node()){
                                    errorMessage.title = "Noeuds libre"
                                    errorMessage.text = "Certaines noeuds du modèle n'appartiennent à aucune barre."
                                    errorMessage.visible = true
                                }
                                else{
                                    if (osup.check_list()){
                                        if (osup.beam_list_empty()){
                                            errorMessage.title = "Vérifier géométrie"
                                            errorMessage.text = "Veuillez créer des barres."
                                            errorMessage.visible = true
                                        }

                                        else{
                                            if (osup.create_file('geo')) {
                                                geolabel.text = "\uE807"
                                                geolabel.color = Theme.success
                                            }
                                        }
                                    }
                                    else {
                                        warningMessage.visible = true
                                    }
                                }
                            }
                        }

                    }
                    Rectangle {
                        height: parent.height
                        width: 70
                        color: "transparent"
//                        ButtonText {
//                            anchors.left: parent.left
//                            anchors.verticalCenter: parent.verticalCenter
//                            text: "Ouvrir"
//                            width: 60
//                            color: Theme.grey_3
//                            onClicked: osup.open_file("geo")
//                        }
                    }
                    Rectangle {
                        height: parent.height
                        width: 140
                        color: "transparent"
                        ButtonText {
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Vérifier la géométrie"
                            color: Theme.grey_3
                            width: 130
                            onClicked: osup.open_file_gmsh()
                        }
                    }
                    Rectangle {
                        height: parent.height
                        width: 40
                        color: "transparent"
                        Label {
                            id: geolabel
                            text: "\uE808"
                            font.family: "fontello"
                            font.pixelSize: 10
                            color: "red"
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 20
                        }
                    }
                }
                Row {
                    width: parent.width
                    height: 50
                    Rectangle {
                        height: parent.height
                        width: parent.width - 320
                        color: "transparent"
                        Label {
                            font.pixelSize: Theme.text
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "-  Fichiers de géométrie <b>.med</b> (format de maillage utilisé par code aster)"
                            anchors.leftMargin: 10

                        }
                    }
                    Rectangle {
                        height: parent.height
                        width: 75
                        color: "transparent"
                        ButtonText {
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Générer"
                            width: 65
                            onClicked:  if (osup.create_file("med")) {
                                            medlabel.text = "\uE807"
                                            medlabel.color = Theme.success
                                        }
                        }
                    }                    
                    Rectangle {
                        height: parent.height
                        width: 210
                        color: "transparent"
                    }
                    Rectangle {
                        height: parent.height
                        width: 40
                        color: "transparent"
                        Label {
                            id: medlabel
                            text: "\uE808"
                            font.family: "fontello"
                            font.pixelSize: 10
                            color: "red"
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 20
                        }
                    }
                }

                Row {
                    width: parent.width
                    height: 50
                    Rectangle {
                        height: parent.height
                        width: parent.width - 320
                        Label {
                            font.pixelSize: Theme.text
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "-  Fichier de scripting <b>.comm</b> :"
                            anchors.leftMargin: 10

                        }
                    }
                    Rectangle {
                        height: parent.height
                        width: 75
                        color: "transparent"
                        ButtonText {
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Générer"
                            width: 65
                            onClicked:{
                                osup.create_file("comm")
                                commlabel.text = "\uE807"
                                commlabel.color = Theme.success
                            }
                        }
                    }
                    Rectangle {
                        height: parent.height
                        width: 210
                        color: "transparent"
                    }
                    Rectangle {
                        height: parent.height
                        width: 40
                        color: "transparent"
                        Label {
                            id: commlabel
                            text: "\uE808"
                            font.family: "fontello"
                            font.pixelSize: 10
                            color: "red"
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 20
                        }
                    }
                }
                Row {
                    width: parent.width
                    height: 50
                    Rectangle {
                        height: parent.height
                        width: parent.width - 320
                        color: "transparent"
                        Label {
                            font.pixelSize: Theme.text
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "-  Fichier de configuration <b>.export</b> "
                            anchors.leftMargin: 10
                        }
                    }
                    Rectangle {
                        height: parent.height
                        width: 75
                        color: "transparent"
                        ButtonText {
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Générer"
                            width: 65
                            onClicked:  if (osup.create_file("export")) {
                                            exportLabel.text = "\uE807"
                                            exportLabel.color = Theme.success
                                        }
                        }
                    }
                    Rectangle {
                        height: parent.height
                        width: 210
                        color: "transparent"
                    }
                    Rectangle {
                        height: parent.height
                        width: 40
                        color: "transparent"
                        Label {
                            id: exportLabel
                            text: "\uE808"
                            font.family: "fontello"
                            font.pixelSize: 10
                            color: "red"
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 20
                        }
                    }
                }
            }
        }
        //--------------------------------------------------------------------------------------
        //MODULE VIDE :FIN D'INSERTION DE CODE

        MessageDialog {
            id: errorMessage
            title: ""
            icon: StandardIcon.Critical
            text: ""
            standardButtons:  StandardButton.Abort
            Component.onCompleted: visible = false
        }
        MessageDialog {
            id: warningMessage
            title: "Aucun ancrage défini"
            icon: StandardIcon.Warning
            text : "Aucun encastrement n'a été défini dans le modèle. Si le modèle est correcte vous pouvez ignorer ce message."
            standardButtons: StandardButton.Yes | StandardButton.Cancel
            Component.onCompleted: visible = false
            onYes: if (osup.create_file('geo')) {
                       geolabel.text = "\uE807"
                       geolabel.color = Theme.success
                   }
        }
    }
}
