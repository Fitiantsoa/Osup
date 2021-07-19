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
    id: pageResult
    background:Rectangle{ color: Theme.background }
    property var temperature: 20

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
                ModuleVerif{
                    objectName: "moduleVerif"
                    Layout.fillWidth: true
                }
                ModuleScript{
                    objectName: "moduleScript"
                    Layout.fillWidth: true
                }
                ModuleStirrup{
                    objectName: "moduleStirrup"
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
                        onClicked: osup.run_aster()
                    }
                    MessageDialog{
                        id: messageDialogErrorFre
                        objectName: "errorGenerate"
                        title: applicationWindow.title
                        standardButtons: StandardButton.Ok
                        icon: StandardIcon.Critical
                    }
                }
                Rectangle{
                    id:fin
                    color:"transparent"
                    width:parent.width
                    height:100
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
