import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.4
import QtQml.Models 2.2
import "../theme.js" as Theme
import QtQuick.Dialogs 1.2

import "../ui"
import "../base"

import MaterialTreeModel 1.0

Page{
    anchors.fill:parent
    property bool isEditable:true
    Rectangle{
        id : rtg1
        anchors.left : parent.left
        anchors.top : parent.top
        anchors.bottom:parent.bottom
        width : parent.width*2/5
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        Rectangle{
            id :tvRect
            anchors.left : parent.left
            anchors.leftMargin: 15
            anchors.top : parent.top
            anchors.bottom:parent.bottom
            anchors.bottomMargin: 15
            width : parent.width - 60
            MaterialTreeModel{
                id :treemodel
            }
            TreeView{
                id : treeView
                anchors.top: parent.top
                anchors.topMargin: 10
                objectName: "treeviewMateriaux"
                anchors.margins: 5
                anchors.right : parent.right
                anchors.bottom:parent.bottom
                anchors.left : parent.left
                visible : true
                model : treemodel
                onClicked:  {
                    lm.clear();
                    treevalue.enabled=false;
                    treevalue.opacity = 0.6;
                    validEdit.enabled = false;
                    rl.enabled=false;
                    treevalue.text = treemodel.data(index);
                    roleLB.text = treemodel.description(index)
                    if (treemodel.hasChildren(index)===false){
                        test.text = "";
                        var content = treemodel.listData(index)[0];
                        lm.append(content)
                    }
                }
                TableViewColumn {
                    title: "Matériaux"
                    role: "name"
                    width: treeView.width
                }
            }
        }
        Rectangle{
            anchors.right : parent.right
            anchors.top : parent.top
            anchors.topMargin: 30
            anchors.bottom:parent.bottom
            anchors.margins: 10
            anchors.left: tvRect.right
            anchors.rightMargin: 0
            ColumnLayout{
                spacing : 10
                ButtonTable{
                    font.pixelSize: 15
                    enabled: isEditable
                    opacity : isEditable?1:0.7
                    text: "\uE826"
                    font.family: "fontello"
                    toolTipText: "Ajouter un élement de même niveau"
                    onClicked: rl.enabled=true
                }
                ButtonTable{
                    text: "\uE812"
                    enabled: isEditable
                    opacity : isEditable?1:0.7
                    font.family: "fontello"
                    font.pixelSize: 15
                    toolTipText: "Supprimer un élement"
                    onClicked: {
                        if (treemodel.selected===false){
                            test.text = "Selectionner l'élement à supprimer "}
                        else {
                            test.text="";
                            treemodel.delNode(treeView.currentIndex)}
                    }
                }
                ButtonTable{
                    text: "\uE819"
                    enabled: isEditable
                    opacity : isEditable?1:0.7
                    font.family: "fontello"
                    toolTipText: "Modifier un élement"
                    font.pixelSize: 15
                    onClicked: {
                        treevalue.enabled=true;
                        treevalue.opacity = 1 ;
                        validEdit.enabled = true}
                }
            }
        }
    }
    Rectangle{
        id : separationRect
        anchors.top : parent.top
        anchors.topMargin: 15
        anchors.bottom:parent.bottom
        anchors.bottomMargin: 15
        anchors.left: rtg1.right
        width:1
        color: Theme.grey_1
        Layout.fillHeight: true

    }
    Rectangle {
        id: rectangle
        anchors.right : parent.right
        anchors.rightMargin: 10
        anchors.top : parent.top
        anchors.bottom:parent.bottom
        anchors.left: separationRect.right
        anchors.leftMargin: 15
        color: "transparent"
        Rectangle{
            id: rectModif
            anchors.bottomMargin: parent.height*3/4
            anchors.right : parent.right
            anchors.top : parent.top
            anchors.bottom:parent.bottom
            anchors.left: parent.left
            anchors.margins: 0
            color: "transparent"
            border.color: Theme.grey_2
            radius : 5
            enabled: isEditable
            ColumnLayout{
                anchors.right : parent.right
                anchors.top : parent.top
                anchors.bottom:parent.bottom
                anchors.left: parent.left
                anchors.margins: 10
                spacing : 30
                ColumnLayout{
                    spacing : 5
                    id : rl
                    enabled : false
                    RowLayout{
                        width:parent.width
                        CTextField{
                            id : tf2
                        }
                        ButtonTable{
                            id : addButton
                            text: "\uE809"
                            font.family: "fontello"
                            font.pixelSize: 15
                            enabled: isEditable
                            opacity : isEditable?1:0.7
                            onClicked: if(tf2.text == ""){
                                           test.text = "Entrer une valeur !"}
                                       else{
                                           treemodel.ajoutNode(treeView.currentIndex,tf2.text)
                                           test.text = ""
                                       }
                        }
                    }
                }
                ColumnLayout{
                    id : cl
                    spacing : 5
                    RowLayout{
                        spacing : 20
                        width:parent.width
                        id : editrow
                        Label{
                            id : roleLB
                            width : 80
                        }
                        CTextField {
                            id : treevalue
                            enabled: false
                            opacity : 0.6
                        }
                        ButtonTable{
                            id :validEdit
                            enabled: isEditable
                            opacity : isEditable?1:0.7
                            font.pixelSize: 12
                            text: "\uE81B"
                            font.family: "fontello"
                            onClicked: treemodel.addDataTitle(treeView.currentIndex,treevalue.text)
                        }
                    }
                    Text{
                        id :test
                        width : 150
                        anchors.horizontalCenter: parent.horizontalCenter
                        color: "red"
                    }
                }
            }
        }
        Rectangle{
            anchors.right : parent.right
            anchors.top : rectModif.bottom
            anchors.bottom:parent.bottom
            anchors.left: parent.left
            anchors.leftMargin: 65
            anchors.margins: 0
            Flickable{
                id : flickable
                anchors.top:parent.top
                anchors.topMargin: 10
                contentWidth: parent.width
                contentHeight: 30
                Rectangle{
                    anchors.fill: parent
                    ListModel{
                        id:lm
                    }
                    Component{
                        id :listDelegate
                        Item{
                            clip:true
                            id: delegateItem
                            width: 400;
                            height: 30
                            property var idx : index
                            RowLayout{
                                spacing : 10
                                anchors.right: parent.right
                                anchors.rightMargin: 10
                                anchors.left: parent.left
                                anchors.leftMargin: 10
                                RowLayout{
                                    spacing:5
                                    Label{
                                        text : "E"
                                    }
                                    CTextField{
                                        id:tfE
                                        text:E
                                        width:50
                                        opacity : 0.5
                                        enabled : false
                                        validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                        onEditingFinished: treemodel.setDataTree(treeView.currentIndex,parseFloat(tfE.text),parseFloat(tfa.text),parseFloat(tfS.text),parseFloat(tfSy.text),parseFloat(tfRm.text))

                                    }
                                }
                                RowLayout{
                                    spacing:5
                                    Label{
                                        text : "a"
                                    }
                                    CTextField{
                                        id:tfa
                                        text:a
                                        width:50
                                        opacity : tfE.opacity
                                        enabled : tfE.enabled
                                        validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                        onEditingFinished: treemodel.setDataTree(treeView.currentIndex,parseFloat(tfE.text),parseFloat(tfa.text),parseFloat(tfS.text),parseFloat(tfSy.text),parseFloat(tfRm.text))

                                    }
                                }
                                RowLayout{
                                    spacing:5
                                    Label{
                                        text : "S"
                                    }
                                    CTextField{
                                        id:tfS
                                        text:S
                                        width:50
                                        opacity : tfE.opacity
                                        enabled : tfE.enabled
                                        validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                        onEditingFinished: treemodel.setDataTree(treeView.currentIndex,parseFloat(tfE.text),parseFloat(tfa.text),parseFloat(tfS.text),parseFloat(tfSy.text),parseFloat(tfRm.text))

                                    }
                                }
                                RowLayout{
                                    spacing:5
                                    Label{
                                        text : "Sy"
                                    }
                                    CTextField{
                                        id:tfSy
                                        text:Sy
                                        width:50
                                        opacity : tfE.opacity
                                        enabled : tfE.enabled
                                        validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                        onEditingFinished: treemodel.setDataTree(treeView.currentIndex,parseFloat(tfE.text),parseFloat(tfa.text),parseFloat(tfS.text),parseFloat(tfSy.text),parseFloat(tfRm.text))

                                    }
                                }
                                RowLayout{
                                    spacing:5
                                    Label{
                                        text : "Rm"
                                    }
                                    CTextField{
                                        id:tfRm
                                        text:Rm
                                        width:50
                                        opacity : tfE.opacity
                                        enabled : tfE.enabled
                                        validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                        onEditingFinished: treemodel.setDataTree(treeView.currentIndex,parseFloat(tfE.text),parseFloat(tfa.text),parseFloat(tfS.text),parseFloat(tfSy.text),parseFloat(tfRm.text))

                                    }
                                }
                                ButtonTable{
                                    id: editButton
                                    enabled: isEditable
                                    opacity : isEditable?1:0.7
                                    text: "\uE819"
                                    font.family: "fontello"
                                    toolTipText: "Modifier"
                                    width:20
                                    onClicked:{
                                        tfE.enabled= true
                                        tfE.opacity=1
                                    }
                                }
                            }
                        }
                    }
                    ListView{
                        id :lv
                        width : 200
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.left: parent.left
                        anchors.topMargin: 20
                        visible: true
                        model : lm
                        delegate: listDelegate
                        ScrollIndicator.vertical: ScrollIndicator {
                            active: true
                            parent: flickable.parent
                        }

                    }
                }
            }
            ButtonTable{
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 15
                enabled: isEditable
                opacity : isEditable?1:0.7
                text: "\uE80E"
                font.family: "fontello"
                fontcolor: Theme.primary
                font.pixelSize: 18
                toolTipText:"Enregister les modifications"
                Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                onClicked: {
                    messageDialog.open()
                }
            }
            MessageDialog {
                id: messageDialog
                title: "Attention !"
                text: "Etes-vous sur de vouloir modifier cette base de données ?"
                standardButtons: StandardButton.Yes |StandardButton.No| StandardButton.Abort
                onYes: {
                    treemodel.nodeToJson()
                }
            }
        }
    }
}





















