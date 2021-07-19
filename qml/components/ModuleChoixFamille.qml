import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import FamilyListModel 1.0
import QtQuick.Dialogs 1.1

import "../theme.js" as Theme
import "../base"
import"../components"
import"../ui"

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
            color: Theme.primary
            text: "\uE815"
            anchors.verticalCenter: parent.verticalCenter
            font.family: "fontello"
            anchors.left: parent.left
            anchors.leftMargin: 2
        }
        Label{
            id:moduletitle
            text:"Importation des familles de supports"
            z:1
            color:Theme.grey_4
            font.pointSize: Theme.title_4
            font.bold:true
            anchors.top: parent.top
            anchors.topMargin: 2
            anchors.left: parent.left
            anchors.leftMargin: 12
        }/*
        OtauButtonTool {
            id: help
            text: "\uE80C"
            font.family: "fontello"
            toolTipText: "Aide"
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.rightMargin: 5
            onClicked:{otau.openManual("page=37")}
        }*/
    }
    Rectangle{
        id: corps
        border.width: 1
        border.color: Theme.grey_4
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
                PropertyChanges { target: corps; height: rectFichier.height+header.height+70+listView.model.count*30}
                PropertyChanges { target: indicateur; text:"\uE815" }
            },
            State {
                name: "closed"
                PropertyChanges { target: corps; height: 0;opacity:0;visible:false}
                PropertyChanges { target: indicateur; text:"\uE818"}
            }
        ]
        transitions: [
            Transition {
                NumberAnimation { duration: 200; properties: "height"}
                NumberAnimation { duration: 200; properties: "opacity"}
                NumberAnimation { duration: 200; properties: "visible"}
            }
        ]
        Rectangle {
            height : 60
            id : rectFichier
            anchors.top : parent.top
            anchors.topMargin: 10
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
                Rectangle{
                    id:rectButtonHaut
                    height:30
                    Layout.fillWidth: true
                    Row {
                        id: row
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        anchors.left: parent.left
                        spacing: 50
                        RowLayout {
                            id: row1
                            anchors.verticalCenter: parent.verticalCenter
                            width : parent.width - 100
                            spacing:10
                            Label {
                                id: label2
                                color: Theme.grey_4
                                Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                                text: qsTr("Dossier du projet : ")
                                anchors.verticalCenter: parent.verticalCenter
                                Layout.preferredWidth: 150
                            }
                            ButtonTable{
                                id: buttonDossierModele2
                                text: "\uF115"
                                anchors.verticalCenter: parent.verticalCenter
                                Layout.preferredHeight: 30
                                Layout.preferredWidth: 30
                                Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                                font.family: "fontello"
                                onClicked: {dialogFolder.open()
                                }
                            }
                            FileDialog {
                                id:dialogFolder;
                                selectFolder: true
                                title: "Choisir le dossier de travail";
                                folder: StandardPaths.standardLocations(StandardPaths.DocumentsLocation)[0]
                                onAccepted: {otauTextField.text = folder}
                            }
                            CTextField {
                                objectName:"FamilyFolderPath"
                                id: otauTextField
                                Layout.fillWidth: true
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }
                        Row {
                            anchors.verticalCenter: parent.verticalCenter
                            width : 70
                            spacing:10
                            ButtonExtract{
                                onClicked: tabDataModel.extract(otauTextField.text)
                            }
                            ButtonRemove{
                                onClicked:{
                                    tabDataModel.erase();
                                    corps.height=rectFichier.height+header.height+70+listView.model.count*30
                                }
                            }
                        }
                    }
                }
                Rectangle{
                    z:1
                    Layout.fillWidth: true
                    height:1
                    color:Theme.otauGrey
                }
            }
        }
        FamilyListModel{
            id :tabDataModel
        }
        Component {
            id: listDelegate
            Item {
                id: delegateItem
                width: listView.width;
                height:30
                clip: true
                RowLayout{
                    anchors.top : parent.top
                    anchors.topMargin: 5
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    spacing : 30
                    CTextField {
                        id:nbTextField
                        text: nb
                        width: 50
                        Layout.maximumWidth: 50
                        Layout.minimumWidth: 50
                        Layout.preferredWidth: 50
                        readOnly: true
                    }
                    CTextField {
                        id:nameTextField
                        text: name
                        width: 150
                        Layout.maximumWidth: 150
                        Layout.minimumWidth: 150
                        Layout.preferredWidth: 150
                        readOnly: true
                    }
                    CCheckBox {
                        id:imprtTextField
                        text: checked? "Oui":"Non"
                        font.bold: true
                        width: 250
                        Layout.maximumWidth: 250
                        Layout.minimumWidth: 250
                        Layout.preferredWidth: 250
                        checked: imprt
                        onCheckStateChanged: tabDataModel.setProperty(index, "imprt", checked)
                    }
                }
            }
        }
        Rectangle {
            id : header
            height : 30
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.top : rectFichier.bottom
            anchors.topMargin:10
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.fillWidth: true
            RowLayout{
                anchors.right: parent.right
                anchors.rightMargin: 10
                anchors.left: parent.left
                anchors.leftMargin: 10
                spacing: 30
                Text {
                    text:"N°"
                    width: 50
                    Layout.preferredWidth: 50
                    font.bold: true
                    color: Theme.otauDarkGrey
                }
                Text {
                    text:"Nom de Famille"
                    width: 150
                    Layout.preferredWidth: 150
                    font.bold: true
                    color: Theme.otauDarkGrey
                }
                Text {
                    text:"Insérer les données dans la note"
                    width: 250
                    Layout.preferredWidth: 250
                    font.bold: true
                    color: Theme.otauDarkGrey
                }
            }
        }
        ListView {
            id :listView
            objectName: "FamilyListView"
            contentWidth: 30
            visible: true
            model :tabDataModel
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 30
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.top: header.bottom
            anchors.topMargin: 10
            delegate :listDelegate
            Layout.fillWidth: true
            onCountChanged: corps.height=rectFichier.height+header.height+50+listView.model.count*30
            ScrollIndicator.vertical: ScrollIndicator { }
        }
    }
}
