import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import QtQuick.Dialogs 1.1

import "../components"
import "../theme.js" as Theme
import "../base"
import "../ui"

import SofixListModel 1.0

Rectangle {
    id: osupModuleSofix
    width: parent.width
    height: title.height + corps.height + 300
    color:"transparent"

    Rectangle {
        id:title
        width: parent.width
        height:  25
        color: "transparent"
        anchors.top: parent.top
        anchors.topMargin: 0
        MouseArea {
            id: mouseArea
            anchors.fill: parent
            onClicked: {
                if (corps.state == "expanded")
                    corps.state = "closed"
                else
                    corps.state = "expanded"
            }
        }
        Row{
            anchors.fill: parent
            anchors.verticalCenter: parent.verticalCenter
            Label {
                id: indicateur
                width: 20
                color: Theme.grey_6
                text: "\uE815"
                anchors.verticalCenter: parent.verticalCenter
                font.family: "fontello"
            }
            Label {
                id:moduletitle
                text:"Etape 2 : Résultats"
                z:1
                color:Theme.grey_6
                font.pixelSize: Theme.text
                font.bold:true
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
    Rectangle{
        id: corps
        border.width: 1
        border.color: Theme.grey_2
        radius: 4
        //color: "transparent"
        anchors.right: parent.right
        anchors.rightMargin: 60
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.top: title.bottom
        anchors.topMargin: 10
        state:"expanded"
        states: [
            State {
                name: "expanded"
                PropertyChanges { target: corps; height: rectlistview.height + 50} // A MODIFIER LE HEIGHT  rectlistview.height + table.height
                PropertyChanges { target: indicateur; text:"\uE815" }
            },
            State {
                name: "closed"
                PropertyChanges { target: corps; height: 0;opacity:0;visible:false}
                PropertyChanges { target: indicateur; text:"\uE818" }

            }
        ]
        transitions: [
            Transition {
                NumberAnimation {duration: 200;properties: "height"}
                NumberAnimation {duration: 200;properties: "opacity"}
                NumberAnimation {duration: 200;properties: "visible"}
            }
        ]
        //MODULE VIDE : INSERER LE CODE CI-DESSOUS
        //--------------------------------------------------------------------------------------
        SofixListModel{
            id: sofixListModel
        }
        Component{
            id: listDelegateSofix
            Item {
                id: delegateItemPlatine
                width: sofixListView.width;
                height: 30
                //                clip: true
                Rectangle {
                    width: corps.width
                    height: parent.height
                    anchors.top: parent.top
                    anchors.topMargin: 30
                    color: "transparent"
                    RowLayout{
                        width: parent.width
                        height: parent.height
                        spacing: 5
//                        Label {
//                            id: tfid
//                            enabled: false
//                            text: id
//                            Layout.preferredWidth: 100
//                            Layout.maximumWidth: 100
//                            Layout.minimumWidth: 100
//                            height: parent.height
//                        }

                        CTextField {
                            id: vx
                            enabled: false
                            text: Vx
                            Layout.preferredWidth: 50
                            Layout.maximumWidth: 50
                            Layout.minimumWidth: 50
                        }
                        CTextField {
                            id: n
                            enabled: false
                            text: N
                            Layout.preferredWidth: 50
                            Layout.maximumWidth: 50
                            Layout.minimumWidth: 50
                        }
                        CTextField {
                            id: vz
                            enabled: false
                            text: Vz
                            Layout.preferredWidth: 50
                            Layout.maximumWidth: 50
                            Layout.minimumWidth: 50
                        }
                        CTextField {
                            id: mx
                            enabled: false
                            text: Mx
                            Layout.preferredWidth: 50
                            Layout.maximumWidth: 50
                            Layout.minimumWidth: 50
                        }
                        CTextField {
                            id: t
                            enabled: false
                            text: T
                            Layout.preferredWidth: 50
                            Layout.maximumWidth: 50
                            Layout.minimumWidth: 50
                        }
                        CTextField {
                            id: mz
                            enabled: false
                            text: Mz
                            Layout.preferredWidth: 50
                            Layout.maximumWidth: 50
                            Layout.minimumWidth: 50
                        }

                        CTextField {
                            id: tfruptCombiAcier
                            text: ruptCombiAcier
                            enabled: false
                            anchors.left: mz.right
                            anchors.leftMargin: 90
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            color : if (tfruptCombiAcier.text >= 1)
                                        tfruptCombiAcier.color = "red";
                                    else
                                        tfruptCombiAcier.color = Theme.primary
                        }
                        CTextField {
                            id: tfruptCombiBet
                            text: ruptCombiBet
                            enabled: false
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            anchors.left: tfruptCombiAcier.right
                            anchors.leftMargin: 140
                            color : if (tfruptCombiBet.text >= 1)
                                        tfruptCombiBet.color = "red";
                                    else
                                        tfruptCombiBet.color = Theme.primary
                        }

                        CTextField {
                            id: tftracmax
                            text: betaN
                            enabled: false
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            anchors.left: tfruptCombiBet.right
                            anchors.leftMargin: 140
                            color : if (tftracmax.text >= 1)
                                        tftracmax.color = "red";
                                    else
                                        tftracmax.color = Theme.primary
                        }
                        Rectangle {
                                id: title
                                width: 25
                                height:  25
                                color: "transparent"
                                anchors.top: parent.top
                                anchors.topMargin: 0
                                anchors.left: tftracmax.right
                                anchors.leftMargin: 0
                                Label {
                                            id: indicateur
                                            width: 20
                                            color: Theme.DarkGrey3
                                            text: "\uE80C"
                                            anchors.verticalCenter: parent.verticalCenter
                                            font.family: "fontello"
                                            anchors.left: parent.left
                                            anchors.leftMargin: 2
                                        }

                                ButtonTable{
                                    id : tabButton
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.right : parent.right
                                    anchors.rightMargin: 5
                                    Popup{
                                        width : 305
                                        height : 90
                                        x: - width
                                        visible: tabButton.survol
                                        Rectangle{
                                            anchors.fill: parent
                                            color: Theme.White
                                            Label{
                                                Layout.preferredWidth: 100
                                                Layout.preferredHeight: 100
                                                text : "Rupture acier : " + ruptacier + "\nRupture extarction glissement : " + ruptExtGliss + "\nRupture cône béton : " + ruptConeBet + "\nRupture fendage : " + ruptFendBet
                                                font.pointSize: 10
                                                font.capitalization: Font.MixedCase
                                                font.weight: Font.Normal
                                                font.family: "Verdana"
                                                font.italic: false
                                                horizontalAlignment: Text.AlignLeft
                                                color: Theme.primary
                                            }
                                        }
                                    }
                                }
                            }

                        CTextField {
                            id: tfcisailmax
                            text: betaV
                            enabled: false
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            color : if (tfcisailmax.text >= 1)
                                        tfcisailmax.color = "red";
                                    else
                                        tfcisailmax.color = Theme.primary
                        }
                        Rectangle {
                                id: title1
                                width: 25
                                height:  25
                                color: "transparent"
                                anchors.top: parent.top
                                anchors.topMargin: 0
                                anchors.left: tfcisailmax.right
                                anchors.leftMargin: 0
                                Label {
                                            id: indicateur1
                                            width: 20
                                            color: Theme.DarkGrey3
                                            text: "\uE80C"
                                            anchors.verticalCenter: parent.verticalCenter
                                            font.family: "fontello"
                                            anchors.left: parent.left
                                            anchors.leftMargin: 2
                                        }
                                ButtonTable{
                                    id : tabButton1
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.right : parent.right
                                    anchors.rightMargin: 5
                                    Popup{
                                        width : 305
                                        height : 75
                                        x: - width
                                        visible: tabButton1.survol
                                        Rectangle{
                                            anchors.fill: parent
                                            color: Theme.White
                                            Label{
                                                Layout.preferredWidth: 100
                                                Layout.preferredHeight: 100
                                                text : "Rupture acier sans bras levier: " + ruptAcierSansBrasLevier + "\nRupture par effet levier : " + ruptEffetLevier  + "\nRupture bord béton : " + ruptBordBet
                                                font.pointSize: 10
                                                font.capitalization: Font.MixedCase
                                                font.weight: Font.Normal
                                                font.family: "Verdana"
                                                font.italic: false
                                                horizontalAlignment: Text.AlignLeft
                                                color: Theme.primary
                                            }
                                        }
                                    }
                                }
                            }

                        ListView.onAdd: SequentialAnimation {
                            PropertyAction { target: delegateItemPlatine; property: "height"; value: 0 }
                            NumberAnimation { target: delegateItemPlatine; property: "height"; to: 30; duration: 250; easing.type: Easing.InOutQuad }
                        }
                        ListView.onRemove: SequentialAnimation {
                            PropertyAction { target: delegateItemPlatine; property: "ListView.delayRemove"; value: true }
                            NumberAnimation { target: delegateItemPlatine; property: "height"; to: 0; duration: 50; easing.type: Easing.InOutQuad }

                            // Make sure delayRemove is set back to false so that the item can be destroyed
                            PropertyAction { target: delegateItemPlatine; property: "ListView.delayRemove"; value: false }
                        }
                    }
                }
            }
        }

        RowLayout{
            Rectangle{
                id : rectlistview
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.leftMargin: 20
                width: corps.width
                height: test1.height
                anchors.topMargin: rectButton.height
                //anchors.bottom: parent.bottom
                //anchors.bottomMargin: 10
                color : "transparent"

                Rectangle {
                    id: test1
                    color:"transparent"
                    height: 30 + osupModuleSofix.count*30
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    width: table.width + rectLeftpart.width
                    ColumnLayout {
                        height: parent.height
                        width: parent.width
                        spacing: 10
                        Rectangle {
                            id: platineHeader
                            color : "transparent"
                            height: 30
                            width: corps.width - 60
                            RowLayout{
                                spacing: 5
                                width: parent.width
                                Text {
                                    text: "Vx"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 50
                                    Layout.maximumWidth: 50
                                    Layout.minimumWidth: 50
                                }
                                Text {
                                    text: "N"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 50
                                    Layout.maximumWidth: 50
                                    Layout.minimumWidth: 50
                                }
                                Text {
                                    text: "Vz"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 50
                                    Layout.maximumWidth: 50
                                    Layout.minimumWidth: 50
                                }
                                Text {
                                    text: "Mx"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 50
                                    Layout.maximumWidth: 50
                                    Layout.minimumWidth: 50
                                }
                                Text {
                                    text: "T"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 50
                                    Layout.maximumWidth: 50
                                    Layout.minimumWidth: 50
                                }
                                Text {
                                    text: "Mz"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 50
                                    Layout.maximumWidth: 50
                                    Layout.minimumWidth: 50
                                }

                                Text {
                                    text: "Rup combi acier"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 100
                                    Layout.maximumWidth: 100
                                    Layout.minimumWidth: 100
                                }
                                Text {
                                    text: "Rup combi bet"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 100
                                    Layout.maximumWidth: 100
                                    Layout.minimumWidth: 100
                                }
                                Text {
                                    text: "Critère max traction"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 100
                                    Layout.maximumWidth: 100
                                    Layout.minimumWidth: 100
                                }
                                Text {
                                    text: "Critère max cisaillement"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                    Layout.preferredWidth: 100
                                    Layout.maximumWidth: 100
                                    Layout.minimumWidth: 100
                                }
                            }
                        }
                        ListView{
                            id: sofixListView
                            objectName: "ListViewSoFix"
                            width: parent.width
                            height: 20 + sofixListModel.count*30
                            model: sofixListModel
                            delegate: listDelegateSofix
                            onCountChanged: {
                                osupModuleSofix.height = sofixListModel.count*30 + 150
                                corps.height = osupModuleSofix.height - 50
                            }
                            ScrollIndicator.vertical: ScrollIndicator {}
                        }
                        MessageDialog {
                            id: errorMessageElem
                            title: " Doublon élément"
                            icon: StandardIcon.Critical
                            text: "L'élément créé existe déjà."
                            standardButtons:  StandardButton.Abort
                            onRejected: console.log("aborted")
                            Component.onCompleted: visible = false
                        }
                    }
                }
            }
        }
    }
}



