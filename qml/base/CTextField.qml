import QtQuick 2.0
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.1
import "../theme.js" as Theme


TextField {
    id: control
    property int size : 60
    placeholderText: qsTr("Enter description")
    Layout.fillWidth: true
    Layout.rowSpan: 2
    Layout.preferredHeight: 30
//    validator: RegExpValidator{regExp:/^[^\/]*$/}
    color: Theme.primary
    selectionColor : Theme.primary
    selectedTextColor: "white"
    hoverEnabled: true
    selectByMouse : true
    onEditingFinished : {focus=false}
    height : 30
    width : size*2
    clip:true
    background: Rectangle {
        implicitWidth: control.size*2
        implicitHeight: 30
        color:"transparent"
        border.color: control.activeFocus ? control.color: Theme.secondary
        border.width: 0 //1.5
        radius: 5
        Rectangle {
            id: rectangle
            height: control.activeFocus ? 2 : 1
            color: control.activeFocus ? control.color: Theme.secondary
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 1
            anchors.rightMargin: 2
            anchors.leftMargin: 2
            anchors.right: parent.right
            anchors.left: parent.left
        }
    }
}
