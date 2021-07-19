import QtQuick 2.6
import QtQuick.Controls 2.1
import "../../Theme.js" as Theme

Switch {
    id: control
    bottomPadding: 0
    indicator: Rectangle {
        implicitWidth: 48*wRatio
        implicitHeight: 26*hRatio
        x: control.leftPadding
        y: parent.height / 2 - height / 2
        radius: 13*average
        border.width: 0
        color: Theme.DarkGrey
        border.color: control.checked ?  Theme.lightColor1 : Theme.darkColor1

        Rectangle {
            x: control.checked ? parent.width - width : 0
            width: 26*Math.max(wRatio, hRatio)
            height: width
            radius: 13*Math.max(wRatio, hRatio)
            border.width: 1
            color:"#ffffff"
            border.color:Theme.LightGrey

        }
    }

    contentItem:Rectangle{
        color :Theme.mainColor1
        border.width: 0
        anchors.left:parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin : control.indicator.width + control.spacing + 10
        Image{
            width: 70*wRatio
            height: width
            opacity: enabled ? 1.0 : 0.3
            source:control.checked ? "../../images/locked.png":"../../images/unlocked.png"
            anchors.centerIn: parent
        }
    }

}
