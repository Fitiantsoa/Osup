import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.0
import "OtauTheme.js" as Theme
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2

Window{
    id : adminpage
    height : 650
    width: 750
    visible : true
    title: "Gestion des droits d'administration"
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
            spacing:30

            Column{
                width:parent.width
                Layout.fillWidth: true
                spacing: content.spacing

                ModuleUser{
                    id : user
                    Layout.fillWidth: true
                }
                ModulePC{
                    id:pc
                    Layout.fillWidth: true
                }
            }
            Rectangle{
                id: rectangle
                color:"transparent"
                height: 200
                Layout.maximumHeight: 200
                Layout.minimumHeight: 200
                Layout.preferredHeight: 200
                Layout.fillHeight: false
                Layout.fillWidth: true

                OtauButtonGenerate{
                    text: qsTr("Modifier<br>les<br>licenses")
                    font.pixelSize: 10
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    anchors.horizontalCenter: parent.horizontalCenter
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    onClicked: if (pc.machineModelCount != 0 & user.userModelCount != 0){
                        messageDialog.visible=true}
                               else{
                        messageDialog2.visible=true    }
                               }

                }
                MessageDialog {
                    id: messageDialog
                    title: "Attention !"
                    text: "Etes-vous sur de vouloir modifier le fichier de license ?
Celui-ci sera définitivement écrasé !
Un redémarrage est nécessaire pour mettre à jour les modifications"
                    standardButtons: StandardButton.Yes |StandardButton.No| StandardButton.Abort
                    onYes: {
                        otau.modifyUser()
                        otau.modifyPC()
                        Qt.quit()
                    }
                }
                MessageDialog {
                    id: messageDialog2
                    title: "Attention !"
                    text: "Impossible de modifier le fichier de license avec une liste vide"
                    standardButtons: StandardButton.Abort
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
                color: Theme.otauGrey
            }

        }

    }
}




