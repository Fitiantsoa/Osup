import QtQuick 2.7
import QtQuick.Controls 2.1
import "../../Theme.js" as Theme

RadioButton {
    property int taille: 15
    property int fontSize: 8
    property color fontColor :"white"
    property color bgColor : Theme.mainColor1
    height : taille + 10
    width : height
    id: control
    text:""
    font.pointSize: fontSize
//    checked: false
    indicator: Rectangle {
        implicitWidth: taille
        implicitHeight: taille
        radius: 3
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        border.width: 1
        border.color: Theme.lightColor1
        opacity: enabled ? 1.0 : 0.4

        Rectangle {
            id: rectangle
            width: taille
            height: taille
            radius: 2
            color: bgColor
            visible: control.checked
            Text {
                id: name
                text: "\uE81C"
                anchors.fill:parent
                anchors.top: parent.top
                font.pixelSize: fontSize * 2
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.family: "fontello"
                color: fontColor
            }
        }
    }
}
