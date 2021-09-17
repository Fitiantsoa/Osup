import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import QtQuick.Dialogs 1.1

import "../components"
import "../theme.js" as Theme
import "../base"
import "../ui"

import PlatineListModelSoFix 1.0

Rectangle {
    id: osupModulePlatine
    width: parent.width
    height: title.height + corps.height + 600
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
                text:"Etape 1 : Chevilles"
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
        //color: "red"
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
                PropertyChanges { target: corps; height: rectlistview.height + table.height} // A MODIFIER LE HEIGHT
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
        PlatineListModelSoFix{
            id: platineModelSoFix
        }
        Component{
            id: listDelegatePlatine
            Item {
                id: delegateItemPlatine
                width: platineListView.width;
                height: 30
                //                clip: true
                Rectangle {
                    width: parent.width
                    height: parent.height
                    color: "transparent"
                    RowLayout{
                        width: parent.width
                        height: parent.height
                        spacing: 20
                        Label {
                            id: tfid
                            enabled: false
                            text: id
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            height: parent.height
                        }
                        CTextField {
                            id: tfdowelNb
                            enabled: false
                            text: dowelsnb
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                        }
                        CTextField {
                            id: modele
                            text: gammeCheville.currentText + " " + modeleCheville.currentText + " " + typeCheville.currentText
                            enabled: false
                            Layout.preferredWidth: 150
                            Layout.maximumWidth: 150
                            Layout.minimumWidth: 100
                        }

                        CTextField {
                            id: tforientation
                            placeholderText: qsTr(" ")
                            text: orientation
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /[XYZ]/}
                        }
                        CTextField {
                            id: vx
                            text: Vx
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /^?\d*([.,]\d+)?$/}
                        }
                        CTextField {
                            id: n
                            text: N
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /^?\d*([.,]\d+)?$/}
                        }
                        CTextField {
                            id: vz
                            text: Vz
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100 
                            validator: RegExpValidator{regExp: /^d*[.,]?\d+$/}
                        }
                        CTextField {
                            id: mx
                            placeholderText: qsTr(" ")
                            text: Mx
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /^d*[.,]?\d+$/}
                        }
                        CTextField {
                            id: t
                            placeholderText: qsTr(" ")
                            text: T
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /^d*[.,]?\d+$/}
                        }
                        CTextField {
                            id: mz
                            text: Mz
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                        }
                        RowLayout{
                            id: rowLayout
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            Layout.maximumWidth: 50
                            ButtonTable{
                                id: editButton
                                toolTipText: "Modifier"
                                text: "\uE819"
                                font.family: "fontello"
                                anchors.verticalCenter: parent.verticalCenter
                                onClicked: {
                                    if (cbaxis.visible === false){
                                        cbaxis.visible =  true
                                        tfaxis.visible = false
                                        tfid.color = "red"
                                    }
                                    else{
                                        cbaxis.visible =  false
                                        tfaxis.visible = true
                                        tfaxis.text = cbaxis.currentText
                                        modele.text = gammeCheville.currentText + " " + modeleCheville.currentText + " " + typeCheville.currentText
                                        platineModelSoFix.setProperty(index, "dowelsnb", tfdowelNb.text)
                                        platineModelSoFix.setProperty(index, "orientation", tforientation.text)
                                        platineModelSoFix.setProperty(index, "Vx", vx.text)
                                        platineModelSoFix.setProperty(index, "N", n.text)
                                        platineModelSoFix.setProperty(index, "Vz", vz.text)
                                        platineModelSoFix.setProperty(index, "Mx", mx.text)
                                        platineModelSoFix.setProperty(index, "T", t.text)
                                        platineModelSoFix.setProperty(index, "Mz", mz.text)
                                        tfid.color = Theme.grey_3
                                    }
                                }
                            }
                            ButtonTable{
                                id: removeButton
                                toolTipText: "Supprimer"
                                text: "\uE808"
                                font.family: "fontello"
                                anchors.verticalCenter: parent.verticalCenter
                                onClicked: {
                                    platineModelSoFix.remove(index);
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

        RowLayout{
            height: parent.height
            width: parent.width - 40
            //            anchors.left: parent.left
            //            anchors.leftMargin: 20
            //            anchors.top: parent.top
            //            anchors.topMargin: 10
            spacing: 10
            Rectangle{
                id:rectButton
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.leftMargin: 20
                width: rectLeftpart.width + table.width  //parent.width
                color: "transparent"
                height: rectLeftpart.height
                //anchors.topMargin: 5
                //anchors.bottom: rectLeftpart.height
                //anchors.bottomMargin: 5
                Row{
                    anchors.fill: parent
                    Rectangle{
                        id: rectLeftpart
                        height : 500 //parent.height
                        width : (osupModulePlatine.width / 3) //(parent.width-320)/2
                        color: "transparent"
                        Column{
                            anchors.fill: parent
                            spacing: 0
                            Rectangle{
                                height : 200
                                width : (parent.width-320)/2
                                color:"transparent"
                                Column{
                                    anchors.fill: parent
                                    spacing: 10
                                    Rectangle{
                                        height : 30
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.top: parent.top
                                        anchors.topMargin: 20
                                        color: "transparent"
                                        RowLayout{
                                            anchors.fill: parent
                                            Label{
                                                Layout.preferredWidth: 150
                                                text : "Nombre de chevilles :"
                                                color : Theme.grey_6
                                            }
                                            CComboBox{
                                                id: nbCheville
                                                objectName: "DowelNumber"
                                                model : ["2","4"]
                                            }
                                        }
                                    }
                                    Rectangle{
                                        height : 30
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.top: parent.top
                                        anchors.topMargin: 70
                                        visible : nbCheville.currentText === "2"
                                        RowLayout{
                                            anchors.fill: parent
                                            Label{
                                                Layout.preferredWidth: 150
                                                text : "Orientation :"
                                                anchors.top: parent.top
                                                color : Theme.grey_6
                                            }
                                            property var or_model
                                            CComboBox{
                                                id: orientation
                                                objectName: "Orientation"
                                                model: ["Vertical", "Horizontal"]
                                            }
                                        }
                                    }
                                }

                            }


                            Rectangle{
                                id: plat2chevImxHor
                                visible: (orientation.currentText === "Horizontal" && nbCheville.currentText === "2")
                                width: 370
                                height: 50
                                color: "transparent"
                                Image{
                                    width: 270
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat2Chev_hor_sof.png"
                                }
                            }
                            Rectangle{
                                id: plat2chevImxVert
                                visible: (orientation.currentText === "Vertical" && nbCheville.currentText === "2")
                                width: 370
                                height: 50
                                color: "transparent"
                                Image{
                                    width: 270
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat2Chev_vert_sof.png"
                                }
                            }

                            Rectangle{
                                id: plat4chevImy
                                visible: (nbCheville.currentText === "4")
                                width: 570
                                height: 50
                                color: "transparent"
                                Image{
                                    width:450
                                    height: 300
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat4Chev_Y_test.png"
                                }
                            }
                        }
                    }

                    Rectangle{
                        height : 500 //parent.height
                        width : (2 * osupModulePlatine.width / 3) - 100 // ((parent.width)/2) + 150
                        color: "transparent"
                        id : table
                        ColumnLayout{
                            anchors.fill: parent
                            anchors.margins: 20
                            spacing: -1

                            RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                Label{
                                    text: "Données géometrique de la platine:"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                    font.bold:true
                                    }
                            }
                            Rectangle{
                                    height : 30
                                    width : table.width
                                    color: "transparent"
                                    id : platinedim
                            RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20


                                Label{
                                    text: "L (mm) :"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: l
                                    objectName: "L"
                                    opacity: enabled?1:0.6
                                    placeholderText: qsTr(" ")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "H (mm) :"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: h
                                    objectName: "H"
                                    placeholderText: qsTr(" ")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "e (mm) :"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: e
                                    objectName: "e"
                                    placeholderText: qsTr(" ")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "a (mm) :"
                                    visible: (nbCheville.currentText === "2" && orientation.currentText == "Horizontal") || (nbCheville.currentText === "4")
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    visible: (nbCheville.currentText === "2" && orientation.currentText == "Horizontal") || (nbCheville.currentText === "4")
                                    id: a
                                    objectName: "a"
                                    placeholderText: qsTr(" ")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "b (mm) :"
                                    visible: (nbCheville.currentText === "2" && orientation.currentText == "Vertical") || (nbCheville.currentText === "4")
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    visible: (nbCheville.currentText === "2" && orientation.currentText == "Vertical") || (nbCheville.currentText === "4")
                                    id: b
                                    objectName: "b"
                                    placeholderText: qsTr(" ")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                }

                            }

                            RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text: "Choix des données materiaux:"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                    font.bold:true
                                    }
                                }
                                Rectangle{
                                    height : 30
                                    width : table.width
                                    color: "transparent"
                                    id : materiauprop
                            RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Rectangle{
                                    height : 30
                                    width : table.width / 4
                                    color: "transparent"
                                    id : rectetat
                            RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text : "Etat :"
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: beton
                                    objectName: "Beton"
                                    implicitWidth: 100
                                    model : ["Fissuré", "Non fissuré"]

                                }
                                }
                                }
                                Rectangle{
                                    height : 30
                                    width : table.width / 4
                                    color: "transparent"
                                    id : rectclass
                            RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                height: 30
//                                Label{
//                                    text : " :"
//                                    Layout.preferredWidth: 50
//                                    color : Theme.grey_6
//                                }
                                Label{
                                    text : "Classe :"
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: classeb
                                    implicitWidth:100
                                    objectName: "ClasseB"
                                    model: ["C20/25", "C25/30", "C30/37", "C35/45", "C40/50", "C45/55", "C50/60"]

                                }
                                }
                                }
                                Rectangle{
                                    height : 30
                                    width : table.width / 4
                                    color: "transparent"
                                    id : rectepaisseur
                            RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text : "Epaisseur (mm) :"
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: epaisseurbeton
                                    objectName: "EpaisseurBeton"
                                    placeholderText: qsTr(" ")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                }
                                }
                                Rectangle{
                                    height : 30
                                    width : table.width / 4
                                    color: "transparent"
                                    id : rectarmature
                            RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                height: 30

                                Label{
                                    text : "Armature :"
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: armature
                                    implicitWidth:50
                                    objectName: "armature"
                                    model: ["Oui", "Non"]

                                }
                                }
                                }
                                }
                                }

                            RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                Label{
                                    text: "Etude:"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                    font.bold:true
                                    }
                            }
                                  Rectangle{
                                    height : 30
                                    width : table.width/2
                                    color: "transparent"
                                    id : rectetude
                            RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                Rectangle{
                                    height : 30
                                    width : table.width/4
                                    color: "transparent"
                                    id : rectedf
                            RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                CCheckBox{
                                            objectName: "EDF"
                                            id:edf
                                            text: "EDF"
                                            checked: true
                                        }
                                        }
                                        }
                                Rectangle{
                                    height : 30
                                    width : table.width/4
                                    color: "transparent"
                                    id : rectnorme
                            RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                Label{
                                    id: labnorme
                                    text: "Norme utilisée:"
                                    Layout.preferredWidth: 100
                                    color : Theme.grey_6
                                    }

                                CComboBox{
                                    id: norme
                                    anchors.left: parent.left
                                    anchors.leftMargin: labnorme.width + 5
                                    implicitWidth: 100
                                    objectName: "Norme"
                                    model: ["Eurocode 2", "ETAG"]
                                }
                                }
                                }
                                }
                                }
                                Rectangle{
                                    height : 30
                                    width : table.width / 2
                                    color: "transparent"
                                    id : etude2
                                RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                Rectangle{
                                    height : 30
                                    width : table.width / 4
                                    color: "transparent"
                                    id : typechargerect
                                RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                Label{
                                    id: labcharge
                                    text: "Type de charge:"
                                    Layout.preferredWidth: 100
                                    color : Theme.grey_6
                                    }
                                CComboBox{
                                    id: typecharge
                                    anchors.left: parent.left
                                    anchors.leftMargin: labcharge.width + 5
                                    implicitWidth: 150
                                    objectName: "TypeCharge"
                                    model: ["Statique ou quasi-statique", "Sismique C1", "Sismique C2"]
                                }
                                }
                                }
                                Rectangle{
                                    height : 30
                                    width : table.width / 4
                                    color: "transparent"
                                    id : situationrect
                                RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                Label{
                                    id: situationlabel
                                    text: "Situation initiale:"
                                    Layout.preferredWidth: 100
                                    color : Theme.grey_6
                                    }
                                CComboBox{
                                    id: situationinitiale
                                    anchors.left: parent.left
                                    anchors.leftMargin: situationlabel.width + 5
                                    implicitWidth: 200
                                    objectName: "SituationInitiale"
                                    model: ["Situations permanentes et transitoires", "Situations accidentelles"]

                                }
                                }
                                }
                                }


                            }
                            RowLayout{
                                spacing: 15
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text: "Choix du type de cheville:"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                    font.bold:true
                                }
                            }
                            Rectangle{
                                    height : 30
                                    width : table.width / 2
                                    color: "transparent"
                                    id : chevilleselect
                            RowLayout{
                                spacing: 10
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Rectangle{
                                    height : 30
                                    width : chevilleselect2.width / 4
                                    color: "transparent"
                                    id : gammerect
                                RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text: "Gamme chevilles :"
                                    Layout.preferredWidth: 100
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: gammeCheville
                                    implicitWidth: 100
                                    objectName: "GammeCheville"
                                    model: ["HILTI", "Würth", "SPIT"]

                                }
                                }
                                }
                                Rectangle{
                                    height : 30
                                    width : chevilleselect2.width / 4
                                    color: "transparent"
                                    id : modelerect
                                RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text: "Modèle chevilles :"
                                    Layout.preferredWidth: 100
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: modeleCheville
                                    implicitWidth: 100
                                    objectName: "ModeleCheville"
                                    model: ["HSL 3-G", "HST3", "HDA-T", "HDA-P"]
                                }
                                }
                                }
                                }
                                }
                                Rectangle{
                                    height : 30
                                    width : table.width / 2
                                    color: "transparent"
                                    id : chevilleselect2
                                RowLayout{
                                spacing: 10
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30

                                Rectangle{
                                    height : 30
                                    width : chevilleselect2.width / 4
                                    color: "transparent"
                                    id : typerect
                                RowLayout{
                                spacing: 0
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    id : typelab
                                    text: "Type chevilles :"
                                    Layout.preferredWidth: 80
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: typeCheville
                                    anchors.left: parent.left
                                    anchors.leftMargin: typelab.width + 15
                                    implicitWidth: 100
                                    objectName: "TypeCheville"
                                    model: ["M8", "M10", "M12", "M16", "M20", "M24"]

                                }
                                }
                                }
                                Rectangle{
                                    height : 30
                                    width : chevilleselect2.width / 4
                                    color: "transparent"
                                    id : profrect
                                RowLayout{
                                spacing: 5
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text: "Profondeur ancrage :"
                                    Layout.preferredWidth: 100
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: profondeurCheville
                                    implicitWidth: 75
                                    objectName: "ProfondeurCheville"
                                    model: ["60", "80", "100"]

                                }

                            }
                            }
                            }
                            }

                            RowLayout{
                                spacing: 10
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text: "Distance aux bords:"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                    font.bold:true
                                }
                            }
                            Rectangle{
                                    height : 30
                                    width : table.width
                                    color: "transparent"
                                    id : distbord
                            RowLayout{
                                spacing: 10
                                width: table.width / 2
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text : "cx0 (mm):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: cx0
                                    objectName: "cx0"
                                    placeholderText: qsTr("1e+15")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "cx1 (mm):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: cx1
                                    objectName: "cx1"
                                    placeholderText: qsTr("1e+15")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "cz0 (mm):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: cz0
                                    objectName: "cz0"
                                    placeholderText: qsTr("1e+15")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "cz1 (mm):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: cz1
                                    objectName: "cz1"
                                    placeholderText: qsTr("1e+15")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                            }
                            }

                            RowLayout{
                                spacing: 10
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text: "Efforts:"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                    font.bold:true
                                }
                            }
                            Rectangle{
                                    height : 30
                                    width : table.width
                                    color: "transparent"
                                    id : effort
                            RowLayout{
                                spacing: 10
                                width: table.width / 2
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                height: 30
                                Label{
                                    text : "Vx (N):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: vx
                                    objectName: "Vx"
                                    placeholderText: qsTr("0")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "N (N):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: n
                                    objectName: "N"
                                    placeholderText: qsTr("0")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "Vz (N):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: vz
                                    objectName: "Vz"
                                    placeholderText: qsTr("0")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "Mx (Nm):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: mx
                                    objectName: "Mx"
                                    placeholderText: qsTr("0")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "T (Nm):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: t
                                    objectName: "T"
                                    placeholderText: qsTr("0")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                                Label{
                                    text : "Mz (Nm):"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: mz
                                    objectName: "Mz"
                                    placeholderText: qsTr("0")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                            }
                            }


                            RowLayout{
                                spacing: 10
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                Rectangle{
                                    color: "transparent"
                                    height: 50
                                    width: 920

                                }
                                ButtonAdd{
                                    anchors.bottom: parent.bottom
                                    anchors.bottomMargin: 5
                                    onClicked: {
                                            if (nbCheville.currentText === "2"){
                                                if (orientation.currentText === "Vertical"){
                                                    platineModelSoFix.append2dwV_sofix(nbCheville.currentText, l.text, h.text,e.text, b.text,orientation.currentText, gammeCheville.currentText, modeleCheville.currentText,
                                        typeCheville.currentText, profondeurCheville.currentText, norme.currentText, typecharge.currentText, situationinitiale.currentText,
                                        cx0.text, cx1.text, cz0.text, cz1.text, beton.currentText, classeb.currentText, epaisseurbeton.text, armature.currentText, edf.checked,
                                        vx.text, n.text, vz.text, mx.text, t.text, mz.text)
                                                }
                                                else{
                                                    platineModelSoFix.append2dwH_sofix(nbCheville.currentText, l.text, h.text, e.text, a.text, orientation.currentText, gammeCheville.currentText, modeleCheville.currentText,
                                        typeCheville.currentText, profondeurCheville.currentText, norme.currentText, typecharge.currentText, situationinitiale.currentText,
                                        cx0.text, cx1.text, cz0.text, cz1.text, beton.currentText, classeb.currentText, epaisseurbeton.text, armature.currentText, edf.checked,
                                        vx.text, n.text, vz.text, mx.text, t.text, mz.text)
                                                }
                                            }
                                            else{
                                                platineModelSoFix.append4dw_sofix(nbCheville.currentText, l.text, h.text,e.text, gammeCheville.currentText, modeleCheville.currentText,
                                        typeCheville.currentText, profondeurCheville.currentText, norme.currentText, typecharge.currentText, situationinitiale.currentText,
                                        cx0.text, cx1.text, cz0.text, cz1.text, beton.currentText, classeb.currentText, epaisseurbeton.text, armature.currentText, edf.checked, b.text, a.text,
                                        vx.text, n.text, vz.text, mx.text, t.text, mz.text)
                                            }
                                        }

                                }
                            }
                            Rectangle{
                                height:1
                                color: Theme.otauGrey
                                Layout.fillWidth: true
                            }
                        }
                    }
                }
            }
            // test
            Rectangle{
                id : rectlistview
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.leftMargin: 20
                width: table.width + rectLeftpart.width
                height: test1.height + 30
                anchors.topMargin: rectButton.height
                //anchors.bottom: parent.bottom
                //anchors.bottomMargin: 10
                color : "transparent"

                Rectangle {
                    id: test1
                    color:"transparent"
                    height: 30 + platineModelSoFix.count*30
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    width: table.width + rectLeftpart.width
                    Column {
                        height: parent.height
                        width: parent.width
                        spacing: 10
                        Rectangle {
                            id: platineHeader
                            color : "transparent"
                            height: 30
                            width: parent.width
                            Row{
                                spacing: 20
                                width: parent.width
                                Text {
                                    text: "N° Cas"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                }
                                Text {
                                    text: "Nombre de chevilles"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 140
                                }
                                Text {
                                    text: " Modèle cheville"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 145
                                }
                                Text {
                                    text: "Orientation"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 145
                                }
                                Text {
                                    text: "Vx (N)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 145
                                }
                                Text {
                                    text: "N (N)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 145
                                }
                                Text {
                                    text: "Vz (N)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 145
                                }
                                Text {
                                    text: "Mx (Nm)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 145
                                }
                                Text {
                                    text: "T (Nm)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 145
                                }
                                Text {
                                    text: "Mz (Nm)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 145
                                }

                            }
                        }
                        ListView{
                            id: platineListView
                            objectName: "PlatineListViewSoFix"
                            width: parent.width
                            height: 40 + platineModelSoFix.count*30
                            model: platineModelSoFix
                            delegate: listDelegatePlatine
                            onCountChanged: {
                                osupModulePlatine.height = 150 + rectLeftpart.height + platineModelSoFix.count*30
                                corps.height = osupModulePlatine.height - 50
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



