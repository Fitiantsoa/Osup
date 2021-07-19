import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.0

import "../theme.js" as Theme
import "../ui"
import RecentFileListModel 1.0

Page{
    background: Rectangle {
    color: Theme.background
        Image{
    //            source:"../../assets/images/bg4.png"
            horizontalAlignment: Image.AlignHCenter
            fillMode: Image.PreserveAspectFit
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            opacity:1
        }
    }
    Rectangle {
        id: rectangle
        color: "transparent"
        anchors.fill: parent
        ColumnLayout {
            id: coll
            width: parent.width
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 100
            spacing: 15
            Image {
                id:imFlex
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                source: "../../assets/images/logoAccueil.png"
                Layout.preferredHeight: 90
                Layout.preferredWidth: 90
                MouseArea{
                    anchors.fill: parent
                    cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                    onClicked:{
                        loader.currentIndex=1;
                    }
                }
            }
            Rectangle {
                height: 150
                width: 200
                color: "transparent"
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Text {
                    color: Theme.grey_6
                    text: qsTr("Commencer un calcul avec OSup")
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.pixelSize: Theme.title_3
                    MouseArea{
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                        onClicked:{
                            loader.currentIndex=1;
                        }
                    }
                }
            }
            Rectangle{
                id:recent
                width: 700
                height: 300
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                color: "Transparent"
                anchors.topMargin: 200
                ColumnLayout{
                    anchors.fill: parent
                    spacing :3
                    RowLayout{
                        Label{
                            width: 550
                            height: 50
                            text : "Fichiers Récents"
                            z:1
                            color:Theme.grey_6
                            font.pointSize: Theme.title_3
                            font.bold:true
                        }
                        Label{
                            id : validlb
                            visible:false
                            color : "green"
                            text: "\uE838"
                            font.family: "fontello"
                            font.pixelSize: 10
                            width : 15
                        }
                    }
                    Rectangle{
                        height: 1
                        width: 700
                        color: Theme.grey_6
                    }
                    Rectangle{
                        id: rectangle1
                        height: 270
                        width : parent.width
                        color : "Transparent"
                        RecentFileListModel{
                            id :lm
                        }
                        Component {
                            id: listDelegate
                            Item {
                                id: delegateItem
                                width: listView.width;
                                height:40
                                clip: true
                                RowLayout{
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    spacing : 20
                                    RecentFileButton{
                                        id:rctfile
                                        nText : numText
                                        pText : pathText
                                        onClicked:{
//                                            var folderP = osup.fileToFolder(rctfile.pText)
                                            osup.read_from_file(rctfile.pText)
                                            validlb.visible=true
                                            loader.currentIndex=1
                                        }
                                    }
                                }
                            }
                        }
                        ListView {
                            id :listView
                            height: 230
                            anchors.leftMargin: 70
                            contentWidth: 40
                            model : lm
                            visible: true
                            objectName: "RecentFileListModel"
                            anchors.bottom: parent.bottom
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.margins : 10
                            delegate :listDelegate
                            Layout.fillWidth: true
                            ScrollIndicator.vertical: ScrollIndicator { }
                        }
                    }
                }
            }
        }
//        Image {
//            id: image
//            anchors.top: recent.bottom
//            anchors.topMargin: 20
//            anchors.horizontalCenter: parent.horizontalCenter
//            sourceSize.height: 50
//            sourceSize.width: 50
//            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//            source: "./images/Otau-logo.png"
//        }
    }
}



