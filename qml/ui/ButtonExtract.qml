import QtQuick 2.6
import "../theme.js" as Theme


//Implementation of the Button control.
Item {
    id: button
    width: 20
    height: 20
    property alias text: label.text;
    property alias font: label.font;
    property color color: Theme.primary
    property color hoverColor: Theme.primary
    property color pressColor: Theme.primary
    property int borderWidth: 0
    property int borderRadius: 100
    scale: state === "Pressed" ? 0.9 : 1.0
//    onEnabledChanged: state = ""
    signal clicked
    signal released

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
        //border.color: "black"

        Text {
            id: label
            x: 6
            y: 6
            font.pixelSize: 15
            text:"\uE82D"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.family: "fontello"
            font.bold:true
            color:"white"
        }
    }

    //change the color of the button in different button states
    states: [
        State {
            name: "Hovering"
            PropertyChanges {
                target: rectangleButton
                opacity: 0.8
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
        onEntered: button.state='Hovering'
        onExited: button.state=''
        onClicked: button.clicked()
        onPressed: button.state="Pressed"
        onReleased: {
            button.released()
            if (containsMouse)
              button.state="Hovering";
            else
              button.state="";
        }
    }
}