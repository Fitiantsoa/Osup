import QtQuick 2.7
import QtQuick.Controls 2.1
import "../theme.js" as Theme

ToolTip {
    id: control
    font.pixelSize: Theme.text
    contentItem: Text {
        text: control.text
        font: control.font
        color: "black"
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.Wrap
    }
    background: Rectangle {
        color: Theme.background
        radius: 4
        border.color : Theme.grey_1
        opacity : 0.8
    }
}
