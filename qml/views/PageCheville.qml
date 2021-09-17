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
    id: pageCheville
    background:Rectangle{ color: Theme.background }
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
                            text:"Les modules suivants permettent de d'effectuer le calcul de chevilles d'ancrages"
                        }
                        Rectangle{
                            height : 1
                            width : parent.width
                            color:Theme.primary
                        }
                    }
                }

                ModulePlatineSofix{
                    objectName: "modulePlatineSofix"
                    Layout.fillWidth: true
                }
                ModuleResultSofix{
                    objectName: "moduleResultSofix"
                    Layout.fillWidth: true
                }

                Rectangle{
                    id: rectangle
                    color:"transparent"
                    height: 100
                    width: parent.width
                    ButtonGenerate{
                        text:"Lancer"
                        anchors.horizontalCenter: parent.horizontalCenter
                        onClicked: {
                            osup.resetSofix()
                            osup.resultSopfix()
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


