import QtQuick 2.6
import QtQuick.Controls 2.1
import "../../Theme.js" as Theme

ProgressBar {
    id: control
    padding: 0
    value : 0
    background: Rectangle {
        implicitWidth: 200*wRatio
        implicitHeight: 6*hRatio
        color: Theme.darkColor1
        radius: 6
    }
    contentItem: Item {
        implicitWidth: 200*wRatio
        implicitHeight: 6*hRatio
        Rectangle {
            objectName: "rectInterieur"
            width: control.value * parent.width
            height: parent.height
            color: "white"
            radius: 6
        }
    }
}
