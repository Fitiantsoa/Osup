import QtQuick 2.6
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.0

import "../theme.js" as Theme

Item {
    id: button
    width: 400
    height: 35
    scale: state === "Pressed" ? 0.9 : 1.0
    onEnabledChanged: state = ""
    property alias text: label.text;
    property alias font: label.font;
    property alias fontcolor: label.color;
    property alias pText : label.text
    property alias nText : num.text
    property color color: "transparent"
    property color hoverColor: Theme.grey_2
    property color pressColor: Theme.grey_2
    property int borderWidth: 0
    property int borderRadius: 10
    property bool survol : state === "Hovering" ? true :false
    signal clicked

    //define a scale animation
    Behavior on scale {
        NumberAnimation {
            duration: 100
            easing.type: Easing.InOutQuad
        }
    }
    //Rectangle to draw the button
    Rectangle {
        id: rectangleButton
        anchors.fill: parent
        radius: borderRadius
        color: button.enabled ? button.color : "transparent"
        border.width: borderWidth
        Row{
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            spacing :10
            Label{
                id : num
                text:numText
                width : 15
                font.pixelSize: 10
            }
            Label{
                text: "\uE843"
                font.family: "fontello"
                font.pixelSize: 10
                width : 15

            }
            Text {
                id: label
                text : pathText
                width: 300
                height: 20
                font.pixelSize: 10
                color:Theme.grey_6
                elide : Text.ElideMiddle
            }
        }
    }
    //change the color of the button in differen button states
    states: [
        State {
            name: "Hovering"

            PropertyChanges{target :label ; color : Theme.otauCyan}
            PropertyChanges{target :label ; font.underline:  true}
        },
        State {
            name: "Pressed"
       }
    ]
    //define transmission for the states
    transitions: [
        Transition {
            from: ""; to: "Hovering"
            ColorAnimation { duration: 50 }
        },
        Transition {
            from: "Hovering"; to: ""
            ColorAnimation { duration: 150 }
        },
        Transition {
            from: "*"; to: "Pressed"
            ColorAnimation { duration: 10 }
        }
    ]
    //Mouse area to react on click events
    MouseArea {
        hoverEnabled: true
        anchors.fill: button
        onEntered: { button.state='Hovering'}
        onExited: { button.state=""}
        onClicked: { button.clicked();}
        onPressed: { button.state="Pressed" }
        onReleased: {
            if (containsMouse)
              button.state="Hovering";
            else
              button.state="";
        }
    }
}


