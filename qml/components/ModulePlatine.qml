import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import QtQuick.Dialogs 1.1

import "../components"
import "../theme.js" as Theme
import "../base"
import "../ui"

import PlatineListModel 1.0

Rectangle {
    id: osupModulePlatine
    width: parent.width
    height: title.height+corps.height
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
                text:"Etape 3 : Platine"
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
                PropertyChanges { target: corps; height: 450}
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
        PlatineListModel{
            id: platineModel
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
                            id: tfaxis
                            text: axis
                            enabled: false
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                        }
                        CComboBox{
                            Component.onCompleted: visible = false
                            id: cbaxis
                            model: ["X", "Y","Z"]
                        }

                        CTextField {
                            id: tforientation
                            enabled: cbaxis.visible
                            placeholderText: qsTr(" ")
                            text: orientation
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /[XYZ]/}
                        }
                        CTextField {
                            id: tfl
                            enabled: cbaxis.visible
                            text: l
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /^?\d*([.,]\d+)?$/}
                        }
                        CTextField {
                            id: tfh
                            enabled: cbaxis.visible
                            text: h
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /^?\d*([.,]\d+)?$/}
                        }
                        CTextField {
                            id: tfe
                            enabled: cbaxis.visible
                            text: e
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100 
                            validator: RegExpValidator{regExp: /^d*[.,]?\d+$/}
                        }
                        CTextField {
                            id: tfa
                            enabled: cbaxis.visible
                            placeholderText: qsTr(" ")
                            text: a
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /^d*[.,]?\d+$/}
                        }
                        CTextField {
                            id: tfb
                            enabled: cbaxis.visible
                            placeholderText: qsTr(" ")
                            text: b
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            validator: RegExpValidator{regExp: /^d*[.,]?\d+$/}
                        }
                        CTextField {
                            id: tfnoeud
                            enabled: cbaxis.visible
                            text: noeud
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                        }
                        Rectangle {
                            color: "transparent"
                            Layout.fillWidth: true
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
                                        platineModel.setProperty(index, "axis", tfaxis.text)
                                        platineModel.setProperty(index, "dowelsnb", tfdowelNb.text)
                                        platineModel.setProperty(index, "orientation", tforientation.text)
                                        platineModel.setProperty(index, "l", tfl.text)
                                        platineModel.setProperty(index, "h", tfh.text)
                                        platineModel.setProperty(index, "e", tfe.text)
                                        platineModel.setProperty(index, "a", tfa.text)
                                        platineModel.setProperty(index, "b", tfb.text)
                                        platineModel.setProperty(index, "noeud", tfnoeud.text)
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
                                    platineModel.remove(index);
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

        Column {
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
                width: parent.width
                anchors.topMargin: 5
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 5
                color: "transparent"
                Row{
                    anchors.fill: parent
                    Rectangle{
                        height : parent.height
                        width : (parent.width-320)/2
                        Column{
                            anchors.fill: parent
                            spacing: 0
                            Rectangle{
                                height : 200
                                width : (parent.width-320)/2
                                Column{
                                    anchors.fill: parent
                                    spacing: 0
                                    Rectangle{
                                        height : 30
                                        anchors.left: parent.left
                                        anchors.right: parent.right
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
                                            Label{
                                                Layout.preferredWidth: 150
                                                text : "Noeud :"
                                                color : Theme.grey_6
                                            }
                                            CComboBox{
                                                id: noeud
                                                objectName: "DowelNode"
                                                model : pageGeo.encas_node_list
                                            }

                                        }
                                    }
                                    Rectangle{
                                        height : 30
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        RowLayout{
                                            anchors.fill: parent
                                            Label{
                                                Layout.preferredWidth: 150
                                                text : "Normal à la platine :"
                                                color : Theme.grey_6
                                            }
                                            CComboBox{
                                                id: axis
                                                objectName: "AxisPlat"
                                                model : ["X","-X","Y","-Y","Z","-Z"]
                                            }
                                        }
                                    }
                                    Rectangle{
                                        height : 30
                                        anchors.left: parent.left
                                        anchors.right: parent.right
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
                                                model: ["Vertical", "Horizontal" ]
                                            }
                                        }
                                    }
                                }

                            }


                            Rectangle{
                                id: plat2chevImxHor
                                visible: (nbCheville.currentText === "2" && (axis.currentText  === "X" || axis.currentText  === "-X") && orientation.currentText === "Horizontal")
                                width: 370
                                height: 50
                                color: "transparent"
                                Image{
                                    width: 270
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/platine2.png"
                                }
                            }
                            Rectangle{
                                id: plat2chevImxVert
                                visible: (nbCheville.currentText === "2" && (axis.currentText  === "X" || axis.currentText  === "-X") && orientation.currentText === "Vertical")
                                width: 370
                                height: 50
                                color: "transparent"
                                Image{
                                    width: 270
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat2Chev_x_Vert.png"
                                }
                            }
                            Rectangle{
                                id: plat2chevImyHor
                                visible: (nbCheville.currentText === "2" && (axis.currentText  === "Y" || axis.currentText  === "-Y") && orientation.currentText === "Horizontal")
                                width: 370
                                height: 50
                                color: "transparent"
                                Image{
                                    width: 270
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat2Chev_y_Hor.png"
                                }
                            }
                            Rectangle{
                                id: plat2chevImyVert
                                visible: (nbCheville.currentText === "2" && (axis.currentText  === "Y" || axis.currentText  === "-Y") && orientation.currentText === "Vertical")
                                width: 370
                                height: 50
                                color: "transparent"
                                Image{
                                    width: 270
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat2Chev_y_Vert.png"
                                }
                            }
                            Rectangle{
                                id: plat2chevImzHor
                                visible: (nbCheville.currentText === "2" && (axis.currentText  === "Z" || axis.currentText  === "-Z") && orientation.currentText === "Horizontal")
                                width: 370
                                height: 50
                                color: "transparent"
                                Image{
                                    width: 270
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat2Chev_z_Hor.png"
                                }
                            }
                            Rectangle{
                                id: plat2chevImVert
                                visible: (nbCheville.currentText === "2" && (axis.currentText  === "Z" || axis.currentText  === "-Z") && orientation.currentText === "Vertical")
                                width: 370
                                height: 50
                                color: "transparent"
                                Image{
                                    width: 270
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat2Chev_z_Vert.png"
                                }
                            }
                            Rectangle{
                                id: plat4chevImx
                                visible: (nbCheville.currentText === "4" && (axis.currentText  === "X" || axis.currentText  === "-X"))
                                width: 570
                                height: 50
                                color: "transparent"
                                Image{
                                    width:450
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat4Chev_X.png"
                                }
                            }
                            Rectangle{
                                id: plat4chevImy
                                visible: (nbCheville.currentText === "4" && (axis.currentText  === "Y" || axis.currentText  === "-Y"))
                                width: 570
                                height: 50
                                color: "transparent"
                                Image{
                                    width:450
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat4Chev_Y.png"
                                }
                            }
                            Rectangle{
                                id: plat4chevImz
                                visible: (nbCheville.currentText === "4" && (axis.currentText  === "Z" || axis.currentText  === "-Z"))
                                width: 570
                                height: 50
                                color: "transparent"
                                Image{
                                    width:450
                                    height:240
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    source:"../../assets/images/Plat4Chev_Z.png"
                                }
                            }

                        }
                    }
                    Rectangle{
                        color: Theme.grey_3
                        anchors.verticalCenter: parent.verticalCenter
                        width: 1
                        height: parent.height-10
                    }
                    Rectangle{
                        height : parent.height
                        width : ((parent.width)/2) - 25
                        id : table
                        Column{
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
                            RowLayout{
                                spacing: 10
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                Label{
                                    text: "Type chevilles :"
                                    Layout.preferredWidth: 100
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: typeCheville
                                    width: 250
                                    objectName: "TypeCheville"
                                    model: ["HILTI HSL 3-G M16", "HILTI HSL 3-G M16", "HDA-P M10"]

                                }
                                Label{
                                    text : "Béton :"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: beton
                                    objectName: "Beton"
                                    width: 150
                                    model : ["Fissuré", "Non fissuré"]

                                }
//                                Label{
//                                    text : " :"
//                                    Layout.preferredWidth: 50
//                                    color : Theme.grey_6
//                                }
                                CComboBox{
                                    id: pression
                                    width:150
                                    objectName: "pression"
                                    model: ["25 MPa", "30 MPa","35 MPa"]

                                }
                                Label{
                                    text : "Epaisseur béton (mm) :"
                                    color : Theme.grey_6
                                }
                                CTextField{
                                    id: epaisseurbeton
                                    objectName: "b"
                                    placeholderText: qsTr(" ")
                                    Layout.preferredWidth: 50
                                    validator: IntValidator{}
                                }
                            }
                            RowLayout{
                                Component.onCompleted: visible=false
                                spacing: 10
                                anchors.right: parent.right
                                anchors.left: parent.left
                                anchors.leftMargin: 15
                                anchors.rightMargin: 20
                                Label{
                                    text: "Production :"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: prod
                                    objectName: "ProdPlatine"
                                    width: 150

                                }
                                Label{
                                    text : "Matériau :"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
                                }
                                CComboBox{
                                    id: mat
                                    objectName: "MatPlatine"
                                    width: 150

                                }
                                Label{
                                    text : "Température  : " + pageGeo.temperature + "  °C"
                                    Layout.preferredWidth: 50
                                    color : Theme.grey_6
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
                                    height: 180
                                    width:920

                                }
                                ButtonAdd{
                                    anchors.bottom: parent.bottom
                                    anchors.bottomMargin: 5
                                    onClicked: {
                                        if (pageGeo.temperature !== ""){
                                            if (nbCheville.currentText === "2"){
                                                if (orientation.currentText === "Vertical"){
                                                    platineModel.append2dwV(nbCheville.currentText, axis.currentText, l.text, h.text,e.text,noeud.currentText,prod.currentText, mat.currentText,pageGeo.temperature, b.text,orientation.currentText )
                                                }
                                                else{
                                                    platineModel.append2dwH(nbCheville.currentText, axis.currentText, l.text, h.text, e.text,noeud.currentText,prod.currentText, mat.currentText,pageGeo.temperature, a.text, orientation.currentText )
                                                }
                                            }
                                            else{
                                                platineModel.append4dw(nbCheville.currentText, axis.currentText, l.text, h.text,e.text,noeud.currentText,prod.currentText, mat.currentText,pageGeo.temperature,b.text, a.text )
                                            }
                                            noeud.model.remove(noeud.currentText)
                                        }
                                        else{
                                            errorMessageElem.title = "Température non défine"
                                            errorMessageElem.text = "Veuillez définir une température dans les conditions de calculs"
                                            errorMessageElem.visible = true
                                        }
                                    }

                                }
                            }
                        }
                    }
                }

            }
            Rectangle{
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.leftMargin: 20
                width: parent.width
                anchors.topMargin: 350
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 10
                Rectangle {
                    width: parent.width
                    height: 1
                    color: Theme.grey_3
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                Rectangle {
                    color:"transparent"
                    height: 30 + platineModel.count*30
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    width: parent.width
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
                                    text: "N° platine"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "Nombre de chevilles"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "Axe normal"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "Orientation"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "L (mm)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "H (mm)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "e (mm)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "a (mm)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "b (mm)"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }
                                Text {
                                    text: "Noeud"
                                    font.bold: true
                                    color: Theme.grey_6
                                    width: 100
                                }

                            }
                        }
                        ListView{
                            id: platineListView
                            objectName: "PlatineListView"
                            width: parent.width
                            height: 40 + platineModel.count*30
                            model: platineModel
                            delegate: listDelegatePlatine
                            onCountChanged: {
                                osupModulePlatine.height = 450 + platineModel.count*30
                                corps.height = 200 + osupModulePlatine.height
                            }
                            ScrollIndicator.vertical: ScrollIndicator { }
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




