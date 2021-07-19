import QtQuick 2.7
import QtQuick.Controls 2.2
import "../../Theme.js" as Theme

Rectangle {
    id: consoleOutput_rectangle
    x: 40
    y: 112
    width: 130
    height: 60
    property TextArea area : control
    property alias font : control.font
    property alias text : control.text
    property alias color : control.color
    property alias readOnly : control.readOnly
    signal editingFinished
    Flickable {
        id: flickable
        anchors.fill: parent
        //        contentWidth: control.width+10
        contentHeight: control.height
        flickableDirection: Flickable.VerticalFlick
        clip: true
        TextArea.flickable:
            TextArea{
            id : control
            color: Theme.mainColor1
            wrapMode: Text.WrapAnywhere
            horizontalAlignment: TextEdit.AlignHCenter
            verticalAlignment: TextEdit.AlignVCenter
            selectByKeyboard: true
            width : consoleOutput_rectangle.width
            selectByMouse: true
            onTextChanged:  consoleOutput_rectangle.editingFinished()
            background: Rectangle {
                color:"transparent"
                //color: control.enabled ? "transparent" : Theme.otauCyan
                border.color: Theme.Grey
                border.width: 0.5
                opacity : 1
                radius:5
                Rectangle {
                    id: rectangle
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 1
                    anchors.rightMargin: 2
                    anchors.leftMargin: 2
                    anchors.right: parent.right
                    anchors.left: parent.left
                }
            }
        }
        ScrollBar.vertical: ScrollBar {
            //                    anchors.bottom: parent.bottom
            anchors.bottomMargin: 3
            //                    anchors.top: parent.top
            anchors.topMargin: 3
            anchors.right: parent.right
            anchors.rightMargin: 0
            visible: control.text!==""?true : false
            contentItem: Rectangle {
                id: rectangle1
                implicitWidth: 10
                implicitHeight: 10
                color :"transparent"
                Rectangle{
                    implicitWidth: 2
                    implicitHeight: parent.height
                    color: Theme.Grey
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                }
            }
        }
    }
}

