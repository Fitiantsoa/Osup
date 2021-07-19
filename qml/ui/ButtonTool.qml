import QtQuick 2.0
import QtQuick.Controls 2.1

import "../theme.js" as Theme
import "../base"

//Implementation of the Button control.
Item {
    id: button
    width: 23
    height: 23
    scale: state === "Pressed" ? 0.9 : 1.0
    onEnabledChanged: state = ""
    property alias text: label.text;
    property alias font: label.font;
    property color color: Theme.grey_1
    property color hoverColor: Theme.grey_2
    property color pressColor: Theme.grey_2
    property int borderWidth: 0
    property int borderRadius: 100
    property bool survol : state === "Hovering" ? true :false
    property alias toolTipText : ott.text
    property alias toolTipx : ott.x
    property alias toolTipy : ott.y
    property alias toolTipParent : ott.parent
    signal clicked

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
        Text {
            id: label
            font.pixelSize: 13
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
                color: hoverColor
            }
        },
        State {
            name: "Pressed"
            PropertyChanges {
                target: rectangleButton
                color: pressColor
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
            ColorAnimation { duration: 500 }
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
        onEntered: { button.state='Hovering' }
        onExited: { button.state='' }
        onClicked: { button.clicked(); }
        onPressed: { button.state="Pressed" }
        onReleased: {
            if (containsMouse)
              button.state="Hovering";
            else
              button.state="";
        }
    }
}
