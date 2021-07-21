import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import "../theme.js" as Theme
import "../base"
import "../ui"

Rectangle {
    id: container
    width: parent.width
    height: title.height+corps.height
    color:"transparent"

    Rectangle {
        id:title
        width: parent.width
        height: 25
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
            color: Theme.grey_3
            text: "\uE815"
            anchors.verticalCenter: parent.verticalCenter
            font.family: "fontello"
            anchors.left: parent.left
            anchors.leftMargin: 2
        }
        Label{
            id:moduletitle
            text:"Note de calcul"
            z:1
            color:Theme.grey_3
            font.pointSize: Theme.title_3
            font.bold:true
            anchors.top: parent.top
            anchors.topMargin: 2
            anchors.left: parent.left
            anchors.leftMargin: 12
        }
        //        OsupButtonLexique {
        //           id: help
        //            text: "\uE80C"
        //            font.family: "fontello"
        //            anchors.top: parent.top
        //            anchors.right: parent.right
        //            anchors.rightMargin: 5
        //            onClicked:{osup.openManual("page=37")}
        //            visible: false
        //        }
        //    }
        Rectangle{
            id: corps
            border.width: 1
            border.color: Theme.grey_5
            radius: 4
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
                    PropertyChanges { target: corps; height: 370}
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
            RowLayout {
                id: row
                spacing: 100
                anchors.fill: parent
                ColumnLayout{
                    anchors.right: row.left
                    anchors.rightMargin: 20
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    spacing: 15
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        Label {
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Référence :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CTextField {
                            objectName: "RefTF"
                            text: ""
                            Layout.fillWidth: true
                            Layout.rightMargin: 100
                        }
                    }
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        Label {
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Client :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CTextField {
                            objectName: "clientTF"
                            text: "SOM CALCUL "
                            Layout.fillWidth: true
                            Layout.rightMargin: 100
                        }
                    }
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        Label {
                            id: label3
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Nom Document :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CTextField {
                            objectName: "DocNameTF"
                            id: osupTextField3
                            text: ""
                            Layout.fillWidth: true
                            Layout.rightMargin: 100
                        }
                    }
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        Label {
                            id: label2
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Rédacteur :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CTextField {
                            objectName: "AuthorTF"
                            id: osupTextField2
                            Layout.fillWidth: true
                            Layout.rightMargin: 100
                        }
                    }
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        Label {
                            id: label1
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Vérificateur :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CTextField {
                            objectName: "SupervisorTF"
                            id: osupTextField1
                            Layout.fillWidth: true
                            Layout.rightMargin: 100
                        }
                    }
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        Label {
                            id: label4
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Approbateur :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CTextField {
                            objectName: "ApproverTF"
                            id: osupTextField4
                            Layout.fillWidth: true
                            Layout.rightMargin: 100
                        }
                    }
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        Label {
                            id: label5
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Nom du Site :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CTextField {
                            objectName: "SiteNameTF"
                            id: osupTextField5
                            Layout.fillWidth: true
                            Layout.rightMargin: 100
                        }
                    }
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        spacing:20
                        Label {
                            id: labelEtat
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Status :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CComboBox {
                            objectName: "StateCC"
                            id: osupTextFieldEtat
                            Layout.preferredWidth: 70
                            model: ["BPO", "BPE"]
                        }
                        Label {
                            id: labelInd
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Version :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CComboBox {
                            objectName: "IndexCC"
                            id: osupTextFieldind
                            Layout.preferredWidth: 70
                            model: ["A", "B", "C", "D", "E"]
                        }
                    }
                    RowLayout {
                        anchors.right: parent.right
                        anchors.rightMargin: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        Label {
                            id: labelDate
                            width: 120
                            color: Theme.grey_4
                            text: qsTr("Date :")
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            Layout.preferredHeight: 30
                            Layout.preferredWidth: 120
                            verticalAlignment: Text.AlignVCenter
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                        }
                        CTextField {
                            objectName: "DateTF"
                            id: osupTextFieldDate
                            placeholderText: "JJ/MM/AAAA"
                            Layout.fillWidth: true
                            Layout.rightMargin: 100
                            validator: RegExpValidator{regExp: /^(0[1-9]|[1-2][0-9]|3[0-1])[/](0[1-9]|1[0-2])[/][0-9]{4}$/}
                        }
                    }
                }
            }
            //--------------------------------------------------------------------------------------
            //MODULE VIDE :FIN D'INSERTION DE CODE

        }
    }
}
