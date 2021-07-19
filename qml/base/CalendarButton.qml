import QtQuick 2.0
import QtQuick.Controls 2.1
import "../../Theme.js" as Theme


//Implementation of the Button control.
Item {
    id: button
    width: 10
    height: 20

    property alias text: label.text;
    property alias font: label.font;
    property color color: "transparent"
    property color hoverColor: "transparent"
    property color pressColor: "transparent"
    property int borderWidth: 0
    property int borderRadius: 100
    scale: state === "Pressed" ? 0.9 : 1.0
    onEnabledChanged: state = ""
    signal clicked

    property bool survol : state === "Hovering" ? true :false

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
            font.pixelSize: 32
            font.bold : true
            anchors.centerIn: parent
            color:"white"
        }
    }

    //change the color of the button in differen button states
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
//            PropertyChanges {
//                target: label
//                color:Theme.otauRed
//            }
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
        onEntered: { button.state='Hovering'}
        onExited: { button.state=''}
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
