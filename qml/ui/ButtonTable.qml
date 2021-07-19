import QtQuick 2.6

import "../theme.js" as Theme
import "../base"


//Implementation of the Button control.
Item {
    id: button
    width: 20
    height: 20
    property alias text: label.text;
    property alias font: label.font;
    property alias fontcolor: label.color;
    property color color: "transparent"
    property color hoverColor: Theme.grey_2
    property color pressColor: Theme.primary
    property int borderWidth: 0
    property int borderRadius: 100
    scale: state === "Pressed" ? 0.9 : 1.0
    onEnabledChanged: state = ""
    signal clicked
    property bool survol : state === "Hovering" ? true :false
    property bool clicked_button: false
    property alias toolTipText : ott.text
    property alias toolTipx : ott.x
    property alias toolTipy : ott.y
    property alias toolTipParent : ott.parent

    CToolTip {
        id :ott
        visible : survol
        delay: 900
    }

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
        //border.color: "black"
        Text {
            id: label
            font.pixelSize: 10
            anchors.centerIn: parent
            color:Theme.grey_6
        }
    }

    //change the color of the button in different button states
    states: [
        State {
            name: "Hovering"
            PropertyChanges {
                target: rectangleButton
                color: primary_lighter_1
            }
        },
        State {
            name: "Pressed"
            PropertyChanges {
                target: rectangleButton
                color: Theme.primary
            }
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
        cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
        onEntered: { button.state='Hovering'}
        onExited: { button.state=""}
        onClicked: {
            button.clicked();
        }
        onPressed: { button.state="Pressed" }
        onReleased: {
            if (containsMouse)
              button.state="Hovering";
            else
              button.state="";
        }
    }
}


