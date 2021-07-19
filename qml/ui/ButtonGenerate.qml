import QtQuick 2.6

import "../theme.js" as Theme

//Implementation of the Button control.
Item {
    id: button
    width: 80
    height: 80
    scale: state === "Pressed" ? 0.9 : 1.0
    property alias text: label.text;
    property alias font: label.font;
    property alias fontsize: label.font.pixelSize;
    property color color: Theme.primary
    property color hoverColor: Theme.primary
    property color pressColor: Theme.primary
    property int borderWidth: 0
    property int borderRadius: 100
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
        radius:borderRadius
        anchors.fill: parent
        color: button.enabled ? button.color : "transparent"
        border.width: borderWidth
        Text {
            id: label
            font.pixelSize: 12
            text:"Génerer"
            anchors.horizontalCenterOffset: 0
            anchors.rightMargin: 0
            anchors.bottomMargin: 1
            anchors.leftMargin: 0
            anchors.topMargin: -1
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.fill: parent
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.bold:true
            color: Theme.grey_1
        }
    }
    //change the color of the button in differen button states
    states: [
        State {
            name: "Hovering"
            PropertyChanges {
                target: rectangleButton
                opacity: 0.9
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
        onEntered: button.state='Hovering'
        onExited: button.state=''
        onClicked: button.clicked()
        onPressed: button.state="Pressed"
        onReleased: {
            if (containsMouse)
              button.state="Hovering";
            else
              button.state="";
        }
    }
}


