import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0

import "../theme.js" as Theme
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
                text:"Module Vide"
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
                PropertyChanges { target: corps; height: 100}
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
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.top : parent.top
            anchors.bottom: parent.bottom
            ColumnLayout{
                spacing : 0
                anchors.fill: parent
            }
        }
        //--------------------------------------------------------------------------------------
        //MODULE VIDE :FIN D'INSERTION DE CODE
    }
}
