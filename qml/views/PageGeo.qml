import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.2
import QtQuick.Extras 1.4
import Qt.labs.platform 1.0
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.0
import QtGraphicalEffects 1.0
import QtQuick.Dialogs 1.1

import "../theme.js" as Theme
import "../base"
import "../ui"
import"../components"

Page{
    id: pageGeo
    background:Rectangle{ color: Theme.background }
    property var encas_node_list
    property var beam_list
    property var node_list
    property var load_node_list
    property var rccm: conditioncaclul.rccm
    property var lvlA: conditioncaclul.lvlA
    property var temperature: 20
    property var porte: 0
    property bool verifTemp: false

    Flickable {
        id: flickable
        anchors.fill: parent
        contentWidth: parent.width
        contentHeight: content.height
        clip:true
        ColumnLayout{
            id: content
            anchors.leftMargin: 70
            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.right: parent.right
            anchors.rightMargin: 70
            anchors.left: parent.left
            spacing: 40
            Column{
                id:monParent
                width:parent.width
                Layout.fillWidth: true
                spacing: content.spacing
                Rectangle{
                    height : 50
                    width : parent.width
                    color: "transparent"
                    Column{
                        height :50
                        width : parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 20
                        Label{
                            color:Theme.primary
                            text:"Les modules suivants permettent de générer la géométrie pour code Aster"
                        }
                        Rectangle{
                            height : 1
                            width : parent.width
                            color:Theme.primary
                        }
                    }
                }
                ModuleCalculationCondition{id: conditioncaclul
                    objectName: "moduleCalculationCondition"
                    Layout.fillWidth: true
                }
                ModuleGeo{
                    objectName: "moduleGeometry"
                    Layout.fillWidth: true
                }
                ModulePlatine{
                    objectName: "modulePlatine"
                    Layout.fillWidth: true
                }
                ModuleStirrup{
                    objectName: "moduleStirrup"
                    Layout.fillWidth: true
                }
                ModuleVerif{
                    objectName: "moduleVerif"
                    Layout.fillWidth: true
                }
//                ModuleScript{
//                    objectName: "moduleScript"
//                    Layout.fillWidth: true
//                }

                Rectangle{
                    id: rectangle
                    color:"transparent"
                    height: 100
                    width: parent.width
                    ButtonGenerate{
                        text:"Lancer"
                        anchors.horizontalCenter: parent.horizontalCenter
                        onClicked: {
                            if (osup.check_pipe_axis()){
                                messageDialogErrorFre.title = "Axe de frottement non défini"
                                messageDialogErrorFre.text = "Veuillez renseigner l'axe de frottement avant de lancer le calcul."
                                messageDialogErrorFre.visible = true
                            }
                            else{
                                if (osup.check_node_load()){
                                    messageDialogErrorFre.title = "Erreur noeud de chargement"
                                    messageDialogErrorFre.text = "Le noeud de chargement est un noeud encastré. Veuillez le modifier avant de relancer le calcul"
                                    messageDialogErrorFre.visible = true
                                }
                                else{
                                    osup.reinitialize_value()
                                    if (osup.check_free_node()){
                                        messageDialogErrorFre.title = "Noeuds libre"
                                        messageDialogErrorFre.text = "Certaines noeuds du modèle n'appartiennent à aucune barre."
                                        messageDialogErrorFre.visible = true
                                    }

                                    if (osup.check_list()){
                                        if (osup.beam_list_empty()){
                                            messageDialogErrorFre.title = "Vérifier géométrie"
                                            messageDialogErrorFre.text = "Veuillez créer des barres."
                                            messageDialogErrorFre.visible = true
                                        }
                                    }
                                    else {
                                        warningMessage.visible = true
                                    }
                                    if (!(osup.check_free_node()) && (osup.check_list()) && !(osup.beam_list_empty())) {
                                        progressbar.value = 0.1
                                        osup.update_widget()
                                        osup.create_file('geo')
                                        console.log("test", osup.check_nb_platine_encas())
                                        if (osup.check_nb_platine_encas()){
                                            osup.create_file("med")
                                            progressbar.value = 0.2
                                            osup.update_widget()
                                            osup.create_file("comm")
                                            osup.create_file("export")
                                            progressbar.value = 0.3
                                            osup.update_widget()
                                            progressbar.value = 0.7
                                            osup.update_widget()
                                            osup.run_aster()
                                            progressbar.value = 1
                                            osup.update_widget()
                                       }
                                       else{
                                            console
                                            progressbar.value = 0
                                            osup.update_widget()
                                            messageDialogErrorFre.title = "Nombre de platines incorrectes"
                                            messageDialogErrorFre.text = "Le nombre de platines ne correspond pas au nombre de noeuds encastrés."
                                            messageDialogErrorFre.visible = true
                                        }
                                    }
                               }
                            }
                        }
                    }
                    Image{
                        width: 20
                        height: 20
                        anchors.right: parent.right
                        source:"../../assets/images/return-icon-512x467-dbhl6xy5.png"
                        MouseArea{
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            onClicked:{
                                loader.currentIndex=0;
                            }
                        }
                    }
                    Text {
                        text: "Retour à la page principale"
                        font.bold: true
                        anchors.top: parent.top
                        anchors.topMargin: 5
                        anchors.right: parent.right
                        anchors.rightMargin: 40
                        color: Theme.grey_6
                        width: 140
                        MouseArea{
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            onClicked:{
                                loader.currentIndex=0;
                            }
                        }
                    }
                    MessageDialog{
                        id: messageDialogErrorFre
                        objectName: "errorGenerate"
                        title: applicationWindow.title
                        text : "Erreur modèle"
                        standardButtons: StandardButton.Ok                        
                        icon: StandardIcon.Critical
                    }
                    MessageDialog {
                        id: warningMessage
                        title: "Aucun ancrage défini"
                        icon: StandardIcon.Warning
                        text : "Aucun encastrement n'a été défini dans le modèle. Si le modèle est correcte vous pouvez ignorer ce message."
                        standardButtons: StandardButton.Yes | StandardButton.Cancel
                        Component.onCompleted: visible = false
                        onYes: osup.create_file('geo')
                    }                    
                }
                Rectangle{
                    id:fin
                    color:"transparent"
                    width:parent.width
                    height:100
                    ProgressBar {
                        anchors.horizontalCenter: parent.horizontalCenter
                        id: progressbar
                        value: 0
                        ProgressBarStyle {
                            background: Rectangle {
                                radius: 2
                                color: "lightgray"
                                border.color: "gray"
                                border.width: 1
                                implicitWidth: 200
                                implicitHeight: 24
                            }
                            progress: Rectangle {
                                color: Theme.primary
                                border.color: Theme.primary_darker_1
                            }
                        }
                    }
                }

            }
        }
        ScrollIndicator.vertical: ScrollIndicator {
            active: true
            parent: flickable.parent
            anchors.top: flickable.top
            anchors.topMargin:10
            anchors.right: flickable.right
            anchors.rightMargin: 10
            anchors.bottom: flickable.bottom
            anchors.bottomMargin:10
            contentItem: Rectangle {
                implicitWidth: 5
                implicitHeight: 50
                color: Theme.grey_6
            }
        }
    }
}


