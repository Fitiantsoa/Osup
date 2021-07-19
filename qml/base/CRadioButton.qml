import QtQuick 2.6
import QtQuick.Controls 2.1
import "../theme.js" as Theme

RadioButton {
    id: control
    text: qsTr("RadioButton")
    checked: true
    indicator: Rectangle {
        id: rectangle
        implicitWidth: 16
        implicitHeight: 16
        x: control.leftPadding
        y: parent.height / 2 - height / 2
        radius: 13
        border.color: control.down ? Theme.primary :Theme.primary
        Rectangle {
            width: 8
            height: 8
            radius: 7
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            color: control.down ? Theme.primary: Theme.primary
            visible: control.checked
        }
    }
    contentItem: Text {
        text: control.text
        font.pixelSize: Theme.text
        opacity: enabled ? 1.0 : 0.3
        color: control.down ? Theme.grey_3 : Theme.grey_6
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        leftPadding: control.indicator.width + control.spacing
    }
}
