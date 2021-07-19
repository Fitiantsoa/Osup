import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.0
import QtQuick.Window 2.2
import Qt.labs.platform 1.0
import QtQuick.Window 2.2
import QtGraphicalEffects 1.0
import "../theme.js" as Theme

import "../components"

Window{
    id : dataManager
    property bool isEditable:true
    visible : true
    objectName:"DataManager"
    height : 650
    title: "Gestion des bases de données"
    width : 1050
    property bool forceClose : false
    onClosing:{
        if(otau.closeDataManager(forceClose)){
            otau.resetDataManager()
            forceClose = false
            close.accepted=true
        }else{
            close.accepted=false
        }
    }
    MessageDialog{
        objectName: "NotSavedDataManager"
        title:"Modification(s) non enregistée(s)"
        buttons: StandardButton.Yes | StandardButton.Cancel
        onYesClicked: {
            dataManager.forceClose = true
            dataManager.close()
        }
    }
    Page{
    id: page
    anchors.fill:parent
        SwipeView {
            id: swipeView
            anchors.fill: parent
            currentIndex: tabBar.currentIndex
            Item {
                PageAdminDBMateriaux{
                    id: materiaux
                    isEditable: dataManager.isEditable
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    anchors.fill: parent
                }
            }
            Item {
                PageAdminDBProfiles{
                    id: sections
                    isEditable: dataManager.isEditable
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    anchors.fill: parent
                }
            }
        }
        header:TabBar {
            id: tabBar
            height:30
            spacing: 0
            anchors.horizontalCenter: parent.horizontalCenter
            background: Rectangle {
                color: Theme.primary
            }
            currentIndex: swipeView.currentIndex
            TabButton {
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                 background: Rectangle {color:swipeView.currentIndex==0 ? Theme.primary: Theme.grey_6}
                contentItem: Text {
                    anchors.fill: parent
                    color : swipeView.currentIndex==0 ? "white": Theme.primary
                    text: "Matériaux"
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }
            TabButton {
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                background: Rectangle {color:swipeView.currentIndex==1 ? Theme.primary: Theme.grey_6}
                contentItem: Text {
                    anchors.fill: parent
                    color : swipeView.currentIndex==1 ? "white": Theme.primary
                    text: "Profilés"
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
    }
}
