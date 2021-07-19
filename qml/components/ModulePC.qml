import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.0
import "OtauTheme.js" as Theme
import QtQuick.Window 2.2
import MachineListModel 1.0
import QtQuick.Dialogs 1.2


Rectangle {
    id: container
    width: parent.width
    height: title.height+corps.height
    color:"transparent"
    property alias machineModelCount: machineModel.count

    Rectangle {
        id:title
        width: 792
        height: 18
        color: "transparent"
        anchors.top: parent.top
        anchors.topMargin: 0

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
        Label {
            id: indicateur
            width: 20
            color: Theme.otauDarkGrey3
            text: "\uE815"
            anchors.verticalCenter: parent.verticalCenter
            font.family: "fontello"
            anchors.left: parent.left
            anchors.leftMargin: 2
        }
        Label{
            id:moduletitle
            text:"Gestion des machines"
            z:1
            color:Theme.otauDarkGrey
            font.pointSize: Theme.otauTitleSize
            font.bold:true
            anchors.top: parent.top
            anchors.topMargin: 2
            anchors.left: parent.left
            anchors.leftMargin: 12
        }

    }

    Rectangle{
        id: corps
        border.width: 1
        border.color: Theme.otauGrey
        radius:Theme.otauModuleRadius
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
                PropertyChanges { target: corps; height:20+listviewCorps.height+ajout.height}
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



            //MODULE VIDE : INSERER LE CODE CI-DESSOUS
            //--------------------------------------------------------------------------------------
        Rectangle {
            color : "transparent"
            height : 80
            id : ajout
            anchors.right : parent.right
            anchors.rightMargin: 10
            anchors.left : parent.left
            anchors.leftMargin: 10
            ColumnLayout{
                spacing : 10
                anchors.right: parent.right
                anchors.rightMargin: 30
                anchors.left: parent.left
                anchors.leftMargin: 30
                anchors.top : parent.top
                anchors.topMargin: 20
                RowLayout {
                    width: parent.width
                    spacing: 10
                    Label {
                        id: label2
                        width: 50
                        color: Theme.otauDarkGrey
                        text: qsTr("Utilisateur principal")
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.preferredHeight: 30
                        Layout.fillWidth: false
                        horizontalAlignment: Text.AlignRight
                    }
                    OtauTextField {
                        objectName:"mainUserTextField"
                        id: otauTextField2
                        Layout.fillWidth: true
                    }
                    Label {
                        id: label
                        width: 50
                        color: Theme.otauDarkGrey
                        text: qsTr("Adresse MAC")
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.preferredHeight: 30
                        Layout.fillWidth: false
                        horizontalAlignment: Text.AlignRight
                    }
                    OtauTextField {
                        objectName:"macTextField"
                        id: otauTextField
                        Layout.fillWidth: true
                    }
                    Label{
                        objectName : "addMacErrorLabel"
                        width: 100
                        text: addButton.enabled ?"" : "Ajout non autorisé"
                        anchors.verticalCenter: parent.verticalCenter
                        color: Theme.otauRed
                    }
                    OtauButtonAdd{
                        id : addButton
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        enabled : adminModifyBool
                        onClicked: {otau.appendPC(otauTextField2.text,otauTextField.text);
                            otauTextField2.text = "";
                            otauTextField.text = ""}
                    }
                }
                Rectangle{
                    height:1
                    color: Theme.otauGrey
                    Layout.fillWidth: true
                }
            }
        }
        Rectangle{
            id: listviewCorps
            height: 50 +listView.model.count * 30
            anchors.top : ajout.bottom
            anchors.topMargin: 10
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.left: parent.left
            anchors.leftMargin: 10

            MachineListModel{
                id: machineModel
            }

            Component {
                id: listDelegate


                Item {
                    id: delegateItem
                    width: listView.width;
                    height:30
                    clip: true

                    Row{
                        anchors.top : parent.top
                        anchors.topMargin: 5
                        anchors.right: parent.right
                        anchors.rightMargin: 10
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        spacing : 200
                        RowLayout{
                            anchors.left:parent.left
                            anchors.leftMargin: 0
                            width : 350
                                OtauTextField {
                                    id:nameTextField
                                    text: name
                                    enabled:false
                                    opacity : enabled ? 1 : 0.3

                                }
                                OtauTextField {
                                    id:macTextField
                                    text: mac
                                    enabled:nameTextField.enabled
                                    opacity : enabled ? 1 : 0.3
                                }
                            }

                        RowLayout{
                            id: rowLayout
                            width: 50
                            anchors.right:parent.right
                            anchors.rightMargin: 20
                            Layout.maximumWidth: 50
                            Layout.minimumWidth: 50
                            Layout.preferredWidth: 50
                            OtauButtonTable{
                                id: editButton

                                text: "\uE819"
                                font.family: "fontello"
                                anchors.verticalCenter: parent.verticalCenter
                                onClicked: nameTextField.enabled=true

                            }
                            OtauButtonTable{
                                id: removeButton
                                text: "\uE808"
                                font.family: "fontello"
                                anchors.verticalCenter: parent.verticalCenter
                                onClicked: {
                                    machineModel.remove(index)
                                    addButton.color = Theme.otauCyan
                                }
                            }
                    }
              }
            }}
            ListView {
                id :listView
                objectName: "machineListView"
                visible: true
                model :machineModel
                anchors.bottom: parent.bottom
                anchors.bottomMargin:10
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.right: parent.right
                anchors.rightMargin: 10
                anchors.top: role.bottom
                anchors.topMargin: 1
                delegate :listDelegate
                ScrollIndicator.vertical: ScrollIndicator { }
                onCountChanged: corps.height=20+listviewCorps.height+ajout.height
}
            Rectangle{
                id : role
                width: parent.width
                height : 18
                color : "transparent"
                Row{
                    anchors.top : parent.top
                    anchors.topMargin: 5
                    anchors.right: parent.right
                    anchors.rightMargin: 20
                    anchors.left: parent.left
                    anchors.leftMargin: 30
                    spacing : 100
                        Text{
                            width: 80
                            text: "Utilisateur principal "
                            id:nom
                            color: Theme.otauDarkGrey
                        }
                        Text{
                            width: 80
                            text: "Adresse MAC"
                            id : prenom
                            color: Theme.otauDarkGrey
                        }
                    }

                    Rectangle{
                        color:"transparent"
                        width : 50
                    }
                }
        }
        }
            //--------------------------------------------------------------------------------------
            //MODULE VIDE :FIN D'INSERTION DE CODE

    }

