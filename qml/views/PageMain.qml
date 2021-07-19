import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.0
import "../theme.js" as Theme

Page{
    id: page
    property alias swipeView : tabBar
    SwipeView {
        id: swipeView
        anchors.fill: parent
        currentIndex: tabBar.currentIndex
        Shortcut{
            sequence: "Right"
            onActivated: {swipeView.currentIndex = (swipeView.currentIndex+1)%3}
        }
        Shortcut{
            sequence: "Left"
            onActivated: {
                if(swipeView.currentIndex == 0){
                    swipeView.currentIndex = 1
                } else {
                    swipeView.currentIndex = swipeView.currentIndex-1
                }
            }
        }
        Item {
            id: item1
            PageGeo {
                anchors.fill: parent
            }
        }
        Item {
            id: item3
            PageSupportNote{
                anchors.fill: parent
            }
        }
    }
    header :TabBar {
        id: tabBar
        height:30
        hoverEnabled: false
        spacing: 0
        anchors.horizontalCenter: parent.horizontalCenter
        currentIndex: swipeView.currentIndex
        TabButton {
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            background: Rectangle {color:swipeView.currentIndex==0 ?Theme.background: Theme.primary }
            contentItem: Text {
                anchors.fill: parent
                color : swipeView.currentIndex==0 ? Theme.primary : Theme.background
                text: "Géométrie"
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }
        TabButton {
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            background: Rectangle {color:swipeView.currentIndex==1 ? Theme.background: Theme.primary }
            contentItem: Text {
                anchors.fill: parent
                color : swipeView.currentIndex==1 ? Theme.primary : Theme.background
                text: "Note de calcul"
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}
