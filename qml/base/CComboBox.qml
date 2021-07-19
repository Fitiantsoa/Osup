import QtQuick 2.6
import QtQuick.Controls 2.1
import "../theme.js" as Theme


ComboBox {
    property alias popupwidth: combopopup.width;
    property color fontColor : Theme.grey_6
    property color bgColor :  "white"
    property color highColor : "white"
    id: control
    implicitWidth: 100
    implicitHeight: 30
    currentIndex : 0
    delegate: ItemDelegate {
        width: combopopup.width
        height: 40
        background:Rectangle{
            color : control.highlightedIndex == index ? Theme.primary: "white"
        }
        contentItem: Text {
            text: modelData
            color: control.highlightedIndex == index ?"white": Theme.primary
            font: control.font
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }
        highlighted: control.highlightedIndex == index
    }
    indicator: Text{
        color: fontColor
        text: "\uE815"
        anchors.right: parent.right
        anchors.rightMargin: 10
        anchors.verticalCenter: parent.verticalCenter
        font.family: "fontello"
        font.pixelSize: control.font.pixelSize
    }
    contentItem: Text {
        id:displayItem
        leftPadding: 2
        rightPadding: control.indicator.width + control.spacing
        text: control.displayText
        font: control.font
        color: fontColor
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
    background: Rectangle {
        color:bgColor
        border.color: bgColor
        border.width: control.visualFocus ? 2 : 1
        radius: 5
    }
    popup: Popup {
        id:combopopup
        y: control.height - 1
        width: control.width
        implicitHeight: listview.contentHeight+20
        padding: 2
        contentItem: ListView {
            id: listview
            contentHeight: 40
            anchors.fill: parent.fill
            clip: true
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            ScrollIndicator.vertical: ScrollIndicator { }
        }
        background: Rectangle {
            color : "white"
            border.color: Theme.grey_1
            radius: 5
        }
    }
}
