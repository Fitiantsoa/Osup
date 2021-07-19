import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.2
import QtQuick.Extras 1.4
import Qt.labs.platform 1.0
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.0
import QtGraphicalEffects 1.0
import QtQuick.Dialogs 1.1

import "../theme.js" as Theme
import "../ui"
import"../components"

Page{
    id: page
    background:Rectangle{ color: Theme.background }
    Flickable {
        id: flickable
        anchors.fill: parent
        contentWidth: parent.width
        contentHeight: content.height
        clip:true
        ColumnLayout{
            id: content
            anchors.leftMargin: 70
            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.right: parent.right
            anchors.rightMargin: 70
            anchors.left: parent.left
            spacing: 50
            Column{
                id:monParent
                width:parent.width
                Layout.fillWidth: true
                spacing: content.spacing
            }
        }
        ScrollIndicator.vertical: ScrollIndicator {
            active: true
            parent: flickable.parent
            anchors.top: flickable.top
            anchors.topMargin:10
            anchors.right: flickable.right
            anchors.rightMargin: 10
            anchors.bottom: flickable.bottom
            anchors.bottomMargin:10
            contentItem: Rectangle {
                implicitWidth: 5
                implicitHeight: 50
                color: Theme.grey_6
            }
        }
    }
}


