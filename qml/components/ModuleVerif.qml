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
    id: osupModuleVerif
    width: parent.width
    height: title.height+corps.height
    color:"transparent"
    Rectangle {
        id:title
        width: parent.width
        height:  25
        color: "transparent"
        anchors.top: parent.top
        anchors.topMargin: 40
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
                anchors.verticalCenter: parent.verticalCenter
                font.family: "fontello"
            }
            Label {
                id:moduletitle
                text:"Etape 5 : Choix de la méthode de vérification du support"
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
            border.width: 1
            border.color: Theme.grey_2
            radius: 4
            anchors.right: parent.right
            anchors.rightMargin: 60
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.top: title.bottom
            anchors.topMargin: 10
            state:"expanded"
            states: [
                State {
                    name: "expanded"
                    PropertyChanges { target: corps; height: 300}
                    PropertyChanges { target: indicateur; text:"\uE815" }
                },
                State {
                    name: "closed"
                    PropertyChanges { target: corps; height: 0;opacity:0;visible:false}
                    PropertyChanges { target: indicateur; text:"\uE818" }

                }
            ]
            transitions: [
                Transition {
                    NumberAnimation {duration: 200;properties: "height"}
                    NumberAnimation {duration: 200;properties: "opacity"}
                    NumberAnimation {duration: 200;properties: "visible"}
                }
            ]
            Rectangle{
            id:rectButton
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 20
            width: parent.width
            anchors.topMargin: 5
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 5
            color: "transparent"

            Rectangle{
                height : parent.height
                width : parent.width-250
                id : table
                Column{
                    anchors.fill: parent
                    anchors.margins: 5
                    spacing: -1
                    RowLayout{
                        spacing: 25
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.leftMargin: 15
                        anchors.rightMargin: 20
                        RowLayout{
                            anchors.fill: parent
                            Label{
                                Layout.preferredWidth: 120
                                text : "Module Osup:"
                                color : Theme.grey_6
                            }
                            CRadioButton{
                                id: ratio
                                objectName: "ModuleRatio"
                                text:"Calcul ratio reglementaire"
                                checked:true
                            }
                            CRadioButton{
                                id: courbe
                                objectName: "ModuleCourbe"
                                text:"Tracé courbe admissible"
                                checked:false
                                onCheckableChanged: {
                                    if (checked){
                                        pageGeo.courbeModule = true
                                    }
                                }
                            }
                        }

                    }
                    RowLayout{
                        id: node
                        spacing: 0
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.leftMargin: 15
                        Label{
                            text : "Noeud de chargement:"
                            anchors.verticalCenter: parent.verticalCenter
                            Layout.preferredWidth: 10
                        }
                        CComboBox {
                            objectName: "NodeLoad"
                            id: nodeLoad
                            model : pageGeo.node_list
                        }
                    }
                    RowLayout{
                        id: caracRatio
                        visible: ratio.checked
                        spacing: 25
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.leftMargin: 15
                        anchors.rightMargin: 20
                        Label{
                            text : "Fx (N):"
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        CTextField {
                            objectName: "Fx"
                            id: fx
                            width: 50
                            placeholderText: ""
                        }
                        Label{
                            text : "Fy (N):"
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        CTextField {
                            objectName: "Fy"
                            id: fy
                            width: 50
                            placeholderText: ""
                        }
                        Label{
                            text : "Fz (N):"
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        CTextField {
                            objectName: "Fz"
                            id: fz
                            width: 50
                            placeholderText: ""
                        }
                    }
                    RowLayout{
                        id: caracCourbe
                        visible: courbe.checked
                        spacing: 10
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.leftMargin: 15
                        anchors.rightMargin: 20
//                        Label{
//                            text : "Frottement max (N):"
//                            anchors.verticalCenter: parent.verticalCenter
//                        }
//                        CTextField {
//                            objectName: "FrictionLoad"
//                            width: 10
//                            text : "1000"
//                            readOnly: true
//                        }
                        Label{
                            text : "Axe tuyauterie :"
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        CComboBox{
                            id: frictionAxis
                            objectName: "FrictionAxis"
                            model: ["X", "Y", "Z"]
                            currentIndex: -1
                        }

                        Label{
                            text : "Nombre de points:"
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        CTextField {
                            objectName: "Points"
                            placeholderText: qsTr("10")
                            id: nbpt
                            width: 10
                        }

                    }                    
                    RowLayout{
                        spacing: 25
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.leftMargin: 15
                        anchors.rightMargin: 20
                        Rectangle {
                            height: 100
                            width: parent.width
                            color: "transparent"
                        }

                        Rectangle {
                            height: 100
                            width: 140
                            color: "transparent"
                            ButtonText {
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: "Vérifier la géométrie"
                                color: Theme.grey_3
                                width: 130
                                onClicked:{
                                    osup.create_file("geo")
                                    osup.open_file_gmsh()
                                }
                            }
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
    }
}
