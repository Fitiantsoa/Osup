import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.2
import QtQuick.Extras 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.0
import QtQuick.Dialogs 1.1
import "../theme.js" as Theme
import "../base"
import"../components"
import "../ui"

Page{
    id: pageRES
    objectName: "PageSupportNote"
    background:Rectangle{color: Theme.background }
    Flickable {
        id: flickable
        anchors.fill: parent
        contentWidth: parent.width
        contentHeight: content.height + 200
        clip:true
        ColumnLayout{
            id: content
            anchors.leftMargin: 70
            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.right: parent.right
            anchors.rightMargin: 70
            anchors.left: parent.left
            spacing:50
            Row{
//                Label {
//                    anchors.verticalCenter: parent.verticalCenter
//                    text:"* : champs à remplir obligatoirement."
//                    color: "red"
//                }
            }
            Column{
                id: column
                width:parent.width
                Layout.fillWidth: true
                spacing: content.spacing
                ModuleNoteDeCalcul{
                    id: moduleNDC
                    objectName : "moduleNoteDeCalcul"
                    Layout.fillWidth: true
                }
                ModuleChoixFamille{
                    id: moduleChoixFamille
                    objectName : "modulehoixFamille"
                    Layout.fillWidth: true
                }
                RowLayout{
                    anchors.horizontalCenter: parent.horizontalCenter
                    spacing : 60
                    ButtonGenerate{
                        id: generateNote
                        text: "Note"
                        onClicked: {
                            osup.extractNote()
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
                //                color: Theme.otauGrey
            }
        }
    }
}
