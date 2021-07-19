import QtQuick 2.7
import QtQuick.Controls 2.1
import "../theme.js" as Theme

CheckBox {
    property alias elide:txt.elide
    property int taille: 18
    property int fontSize: Theme.text
    id: control
    text:"CheckBox"
    font.pixelSize: fontSize
    checked: false
    indicator: Rectangle {
        implicitWidth: taille
        implicitHeight: taille
        x: control.leftPadding
        y: parent.height / 2 - height / 2
        radius: 3
        border.width: 1
        border.color: Theme.primary
        opacity: enabled ? 1.0 : 0.4

        Rectangle {
            width: taille
            height: taille
            radius: 2
            color: control.down ? Theme.primary : Theme.primary
            visible: control.checked
            Text {
                id: name
                text: "\uE81C"
                anchors.fill: parent
                font.pixelSize: 16
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.family: "fontello"
                color: "white"
            }
        }
    }

    contentItem: Text {
        id:txt
        text: control.text
        anchors.left: parent.left
        anchors.leftMargin: 20+taille
        anchors.right: parent.right
        anchors.rightMargin: 0
        font: control.font
        opacity: enabled ? 1.0 : 0.4
        color: Theme.primary
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
    }
}
