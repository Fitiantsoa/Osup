import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.4
import QtQml.Models 2.2
import QtQuick.Dialogs 1.2

import "../theme.js" as Theme
import "../base"
import "../ui"

import  ProfileTreeModel 1.0

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
            ProfileTreeModel{
                id :treemodel
            }
            TreeView{
                id : treeView
                anchors.top: parent.top
                anchors.topMargin: 10
                objectName: "treeviewSections"
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
                        console.log(treemodel.listData(index))
                        var content = treemodel.listData(index)[0];
                        osup.print(content)
                        lm.append(content)
                    }
                }
                TableViewColumn {
                    title: "Profilé"
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
                    font.family: "fontello"
                    font.pixelSize: 15
                    enabled: isEditable
                    opacity : isEditable?1:0.7
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
                        validEdit.enabled = true
                    }
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
                        Label{
                            text:"Ajouter l'élément suivant : "
                            opacity: enabled ? 1 : 0.2
                        }
                        CTextField{
                            id : tf2
                            placeholderText: "Nouvel élément"
                        }
                        ButtonTable{
                            id : addButton
                            enabled: isEditable
                            opacity : isEditable?1:0.7
                            text: "\uE81B"
                            font.family: "fontello"
                            font.pixelSize: 12
                            toolTipText: "Valider nouvel élément"
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
                            font.pixelSize: 12
                            text: "\uE81B"
                            font.family: "fontello"
                            toolTipText: "Valider la modification"
                            onClicked: treemodel.addDataTitle(treeView.currentIndex,treevalue.text)
                            enabled: false
                        }
                    }
                    Text{
                        id :test
                        width : 150
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
            anchors.margins: 0
            Flickable{
                id : flickable
                anchors.top:parent.top
                anchors.topMargin: 10
                contentWidth: parent.width
                contentHeight: 320
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
                            width: 600;
                            height: 120
                            property var idx : index
                            Row{
                                width: parent.width
                                height: parent.height
                                Column {
                                    width: parent.width - 30
                                    height: 150
                                    Row {
                                        width: parent.width
                                        height: 30
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "h(mm)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfh
                                                    text: h
                                                    width:60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : 0.5
                                                    enabled : false
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "b(mm)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfb
                                                    text: b
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "tw(mm)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tftw
                                                    text: tw
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "tf(mm)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tftf
                                                    text: tf
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                    }
                                    Row {
                                        width: parent.width
                                        height: 30
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Aire(mm2)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfaire
                                                    text: aire
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Sy(mm2)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfsy
                                                    text: sy
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Sz(mm2)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfsz
                                                    text: sz
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Wy(mm)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfwy
                                                    text: h
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                    }
                                    Row {
                                        width: parent.width
                                        height: 30
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Wz(mm2)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfwz
                                                    text: wz
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Ig(cm4)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfig
                                                    text: ig
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Iy(cm4)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfiy
                                                    text: sz
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Iz(cm4)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfiz
                                                    text: iz
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                    }
                                    Row {
                                        width: parent.width
                                        height: 30
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Igr(cm3)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfigr
                                                    text: igr
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Wely(cm3)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfwely
                                                    text: wely
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Wply(cm3)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfwply
                                                    text: wply
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Welz(cm3)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfwelz
                                                    text: welz
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                    }
                                    Row {
                                        width: parent.width
                                        height: 30
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Wplz(cm3)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfwplz
                                                    text: wplz
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Iw(cm6)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfiw
                                                    text: iw
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled : tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Vy(mm)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfvy
                                                    text: vy
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                        Rectangle {
                                            width: parent.width/4
                                            height: parent.height
                                            Row{
                                                spacing:5
                                                Label{
                                                    text : "Vx(mm)"
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                }
                                                CTextField{
                                                    id: tfvx
                                                    text: vx
                                                    width: 60
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    opacity : tfh.opacity
                                                    enabled :  tfh.enabled
                                                    validator: RegExpValidator{regExp: /^[0-9]*\.?[0-9]+/}
                                                    onEditingFinished: treemodel.setDataTree(treeView.currentIndex,
                                                                                             parseFloat(tfh.text),
                                                                                             parseFloat(tfb.text),
                                                                                             parseFloat(tftw.text),
                                                                                             parseFloat(tftf.text),
                                                                                             parseFloat(tfaire.text),
                                                                                             parseFloat(tfsy.text),
                                                                                             parseFloat(tfsz.text),
                                                                                             parseFloat(tfwy.text),
                                                                                             parseFloat(tfwz.text),
                                                                                             parseFloat(tfig.text),
                                                                                             parseFloat(tfiy.text),
                                                                                             parseFloat(tfiz.text),
                                                                                             parseFloat(tfigr.text),
                                                                                             parseFloat(tfwely.text),
                                                                                             parseFloat(tfwply.text),
                                                                                             parseFloat(tfwelz.text),
                                                                                             parseFloat(tfwplz.text),
                                                                                             parseFloat(tfiw.text),
                                                                                             parseFloat(tfvy.text),
                                                                                             parseFloat(tfvx.text))
                                                }
                                            }
                                        }
                                    }
                                }
                                ButtonTable{
                                    id: editButton
                                    text: "\uE819"
                                    anchors.verticalCenter: parent.verticalCenter
                                    width: 20
                                    font.family: "fontello"
                                    toolTipText: "Modifier"
                                    onClicked:{
                                        tfh.enabled= true
                                        tfh.opacity=1
                                    }
                                }
                            }
                        }
                    }
                    ListView{
                        id :lv
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.left: parent.left
                        anchors.topMargin: 20
                        visible: true
                        model : lm
                        delegate: listDelegate
                        ScrollIndicator.vertical: ScrollIndicator {
                            visible: lv.visible
                            anchors.right: lv.right
                            contentItem: Rectangle {
                                implicitWidth: 3
                                implicitHeight: 50
                                color: Theme.grey_1
                            }
                        }
                    }
                }
            }
            ButtonTable{
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 15
                text: "\uE80E"
                font.family: "fontello"
                fontcolor: Theme.primary
                font.pixelSize: 18
                enabled: isEditable
                opacity : isEditable?1:0.7
                toolTipText:"Enregister les modifications"
                Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                onClicked:{
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



















