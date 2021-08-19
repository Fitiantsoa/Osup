import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import QtQuick.Dialogs 1.1

import "../theme.js" as Theme
import "../base"
import "../ui"
import "../components"

import NodeListModel 1.0
import BeamListModel 1.0

Rectangle {
    property bool verifTemp: false
    id: container
    width: parent.width
    height: title.height+corps.height
    color:"transparent"
    Rectangle {
        id:title
        width: 792
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
                font.family: "fontello"
                anchors.verticalCenter: parent.verticalCenter
            }
            Label{
                id:moduletitle
                text:"Etape 2 : Définition de la géométrie"
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
        color : "transparent"
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.top: title.bottom
        anchors.topMargin: 10
        state:"expanded"
        states: [
            State {
                name: "expanded"
                PropertyChanges { target: corps; height: 600}
                PropertyChanges { target: indicateur; text: "\uE815" }
            },
            State {
                name: "closed"
                PropertyChanges { target: corps; height: 0;opacity:0;visible:false}
                PropertyChanges { target: indicateur; text: "\uE818" }

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
        NodeListModel{
            id: nodeModel
        }
        Component{
            id: listDelegateNode
            Item {
                id: delegateItemNode
                width: nodeListView.width;
                height: 30
                Rectangle {
                    width: parent.width
                    height: parent.height
                    color: "transparent"
                    RowLayout{
                        width: parent.width
                        height: parent.height
                        spacing: 20
                        Label {
                            id: idtext
                            enabled: false
                            text: id
                            Layout.preferredWidth: 100
                            Layout.maximumWidth: 100
                            Layout.minimumWidth: 100
                            height: parent.height
                        }
                        CTextField {
                            id: tfx
                            enabled: false
                            text: cx
                            Layout.preferredWidth: 120
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            validator: RegExpValidator{regExp: /^?\d*([.,]\d+)?$/}
                        }
                        CTextField {
                            id: tfy
                            enabled: tfx.enabled
                            text: cy
                            Layout.preferredWidth: 120
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            validator: RegExpValidator{regExp: /^?\d*([.,]\d+)?$/}
                        }
                        CTextField {
                            id: tfz
                            enabled: tfx.enabled
                            text: cz
                            Layout.preferredWidth: 120
                            Layout.maximumWidth: 120
                            Layout.minimumWidth: 120
                            validator: RegExpValidator{regExp: /^?\d*([.,]\d+)?$/}
                        }
                        CTextField {
                            Component.onCompleted: visible = true
                            id: tfap
                            text: ap
                            placeholderText: qsTr("Libre")
                            Layout.preferredWidth: 300
                            Layout.maximumWidth: 300
                            Layout.minimumWidth: 300
                        }
                        CComboBox {
                            Component.onCompleted: visible = false
                            id: appui_modif
                            model: ["Libre","Encastrement","DX", "DX DY","DX DY DZ","DX DY DZ DRX","DX DY DZ DRX DRY","DX DY DZ DRX DRZ","DX DY DZ DRY","DX DY DZ DRY DRZ", "DX DZ", "DY", "DY DRX DRZ","DY DZ","DY DZ DRX DRZ", "DZ"]
                            width: 250
                            height: 40                            
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
                                    if (!appui_modif.visible){
                                        tfx.enabled=true;
                                        tfap.visible = false
                                        appui_modif.visible = true
                                        tfn1.text = ""
                                        tfn2.text = ""
                                        idtext.color = "red"
                                    }
                                    else{
                                        tfap.text = appui_modif.currentText
                                        nodeModel.setProperty(index, "ap", appui_modif.currentText)
                                        nodeModel.setProperty(index, "cx", tfx.text)
                                        nodeModel.setProperty(index, "cy", tfy.text)
                                        nodeModel.setProperty(index, "cz", tfz.text)
                                        tfx.enabled=false
                                        appui_modif.visible = false
                                        tfap.visible = true
                                        idtext.color = Theme.grey_3
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
                                    nodeModel.remove(index);                                    
                                }
                            }
                        }
                    }
                }
                ListView.onAdd: SequentialAnimation {
                    PropertyAction { target: delegateItemNode; property: "height"; value: 0 }
                    NumberAnimation { target: delegateItemNode; property: "height"; to: 30; duration: 250; easing.type: Easing.InOutQuad }
                }
                ListView.onRemove: SequentialAnimation {
                    PropertyAction { target: delegateItemNode; property: "ListView.delayRemove"; value: true }
                    NumberAnimation { target: delegateItemNode; property: "height"; to: 0; duration: 50; easing.type: Easing.InOutQuad }

                    // Make sure delayRemove is set back to false so that the item can be destroyed
                    PropertyAction { target: delegateItemNode; property: "ListView.delayRemove"; value: false }
                }
            }
        }
        BeamListModel{
            id: beamModel
        }
        Component{
            id: listDelegateBeam
            Item {
                id: delegateItemBeam
                width: beamListView.width;
                height: 30
                clip: true
                RowLayout{
                    width: parent.width
                    height: parent.height
                    spacing: 20
                    Label {
                        id:idbeam
                        enabled: false
                        text: id
                        Layout.preferredWidth: 100
                        Layout.maximumWidth: 100
                        Layout.minimumWidth: 100
                        height: parent.height
                    }
                    CTextField {
                        id:tfn1
                        enabled: false
                        text: n1
                        Layout.preferredWidth: 100
                        Layout.maximumWidth: 100
                        Layout.minimumWidth: 100
                        onFocusChanged: beamModel.setProperty(index, "n1", tfn1.text)
                        validator:  RegExpValidator{regExp: /^[0-9][0-9]?$/}
                    }
                    CTextField {
                        id: tfn2
                        enabled: tfn1.enabled
                        text: n2
                        Layout.preferredWidth: 100
                        Layout.maximumWidth: 100
                        Layout.minimumWidth: 100
                        onFocusChanged: beamModel.setProperty(index, "n2", tfn2.text)
                        validator:  RegExpValidator{regExp: /^[0-9][0-9]?$/}
                    }
                    CTextField {
                        id: tfprod
                        enabled: false
                        text: prod
                        readOnly: true
                        Layout.preferredWidth: 200
                        Layout.maximumWidth: 200
                        Layout.minimumWidth: 200
                        validator:  RegExpValidator{regExp: /^?\d*([.,]\d+)?$/}
                    }
                    CComboBox{
                        Component.onCompleted: visible = false
                        id: productionModif
                        width: 140
                        model: production.model
                    }
                    CTextField {
                        id: tfmat
                        enabled: false
                        text: mat
                        readOnly: true
                        Layout.preferredWidth: 200
                        Layout.maximumWidth: 200
                        Layout.minimumWidth: 200 
                    }
                    CComboBox{
                        Component.onCompleted: visible = false
                        id: materiauModif
                        width: 140
                        model: materiau.model
                    }
                    CTextField {
                        id: tfsec
                        enabled: tfn1.enabled
                        text: sec
                        readOnly: true
                        Layout.preferredWidth: 200
                        Layout.maximumWidth: 200
                        Layout.minimumWidth: 200
                        validator: RegExpValidator{regExp: /^[-]?\d*[.,]?\d+$/}
                    }
                    CComboBox{
                        Component.onCompleted: visible = false
                        id: secModif
                        width: 140
                        model: section.model
                    }
                    CComboBox{
                        Component.onCompleted: visible = false
                        id: dimModif
                        width: 140
                        model: dimension.model
                    }
                    CTextField {
                        id: tfor
                        enabled: tfn1.enabled
                        text: or
                        Layout.preferredWidth: 200
                        Layout.maximumWidth: 200
                        Layout.minimumWidth: 200
                        onFocusChanged: beamModel.setProperty(index, "or", tfor.text)
                        validator:  RegExpValidator{regExp: /^[-]?\d*[.,]?\d+$/}
                    }
                    Rectangle {
                        color: "transparent"
                        Layout.fillWidth: true
                    }
                    RowLayout{
                        id: rowLayout
                        anchors.verticalCenter: parent.verticalCenter
                        Layout.maximumWidth: 50
                        ButtonTable{
                            id: editButton
                            toolTipText: "Modifier"
                            text: "\uE819"
                            font.family: "fontello"
                            anchors.verticalCenter: parent.verticalCenter
                            onClicked: {
                                if (!productionModif.visible){
                                    idbeam.color = "red"
                                    tfn1.enabled=true;
                                    productionModif.visible = true
                                    productionModif.currentIndex = production.currentIndex
                                    materiauModif.visible = true
                                    materiauModif.currentIndex = materiau.currentIndex
                                    secModif.visible = true
                                    secModif.currentIndex = section.currentIndex
                                    dimModif.visible = true
                                    dimModif.currentIndex = dimension.currentIndex
                                    tfmat.visible = false
                                    tfprod.visible = false
                                    tfsec.visible = false
                                }
                                else{
                                    idbeam.color = Theme.grey_3
                                    tfn1.enabled=false;
                                    tfprod.text = productionModif.currentText
                                    tfmat.text = materiauModif.currentText
                                    tfsec.text = secModif.currentText + dimModif.currentText
                                    beamModel.setProperty(index, "mat", materiauModif.currentText)
                                    beamModel.setProperty(index, "prod", productionModif.currentText)
                                    beamModel.setProperty(index, "sec", secModif.currentText +" "+ dimModif.currentText)
                                    productionModif.visible = false
                                    materiauModif.visible = false
                                    secModif.visible = false
                                    dimModif.visible = false
                                    tfmat.visible = true
                                    tfprod.visible = true
                                    tfsec.visible = true
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
                                beamModel.remove(index);
                            }
                        }
                    }
                }
                ListView.onAdd: SequentialAnimation {
                    PropertyAction { target: delegateItemBeam; property: "height"; value: 0 }
                    NumberAnimation { target: delegateItemBeam; property: "height"; to: 30; duration: 250; easing.type: Easing.InOutQuad }
                }
                ListView.onRemove: SequentialAnimation {
                    PropertyAction { target: delegateItemBeam; property: "ListView.delayRemove"; value: true }
                    NumberAnimation { target: delegateItemBeam; property: "height"; to: 0; duration: 50; easing.type: Easing.InOutQuad }

                    // Make sure delayRemove is set back to false so that the item can be destroyed
                    PropertyAction { target: delegateItemBeam; property: "ListView.delayRemove"; value: false }
                }
            }
        }

        Rectangle{
            color : "transparent"
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.top : parent.top
            anchors.bottom: parent.bottom
            Column {
                spacing : 0
                anchors.fill: parent
                Label {
                    text: "Noeuds"
                    height: 30
                    anchors.left: parent.left
                    font.pixelSize: Theme.title_3
                    color: Theme.grey_6
                }
                Rectangle {
                    id: nodeModule
                    border.color: Theme.grey_2
                    border.width: 1
                    radius: 4
                    width: corps.width - 60
                    state:"expanded"
                    states: [
                        State {
                            name: "expanded"
                            PropertyChanges { target: nodeModule; height: 230 + nodeModel.count*30}
                        },
                        State {
                            name: "closed"
                            PropertyChanges { target: nodeModule; height: 0;opacity:0;visible:false }
                            PropertyChanges { target: corps; height: 100 + beamModule.height ;opacity:100;visible:true}
                        }
                    ]
                    transitions: [
                        Transition {
                            NumberAnimation {duration: 200;properties: "height"}
                            NumberAnimation {duration: 200;properties: "opacity"}
                            NumberAnimation {duration: 200;properties: "visible"}
                        }
                    ]
                    Column {
                        height: parent.height
                        width: parent.width - 40
                        anchors.left: parent.left
                        anchors.leftMargin: 20
                        anchors.top: parent.top
                        anchors.topMargin: 10
                        spacing: 10
                        Rectangle {
                            color : "transparent"
                            height: 35
                            width: parent.width
                            Row{
                                anchors.right: parent.right
                                anchors.rightMargin: 0
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                spacing: 5
                                Row {
                                    width: parent.width - 30
                                    height: parent.height
                                    spacing: 30
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Position X (mm) :"
                                            anchors.verticalCenter: parent.verticalCenter                                            
                                        }
                                        CTextField {
                                            id: tfcx
                                            width: 80
                                            //validator: RegExpValidator{regExp: /^[0]{0,1}[.][0-9]{0,1}([0-9]{0,1})?([0-9]{0,1})?/}
                                        }
                                        Shortcut{
                                            sequence: "right"
                                            onActivated: {
                                                tfcy.text = "12"
                                                tfcy.activeFocus
                                           }
                                       }
                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Position Y (mm) :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CTextField {
                                            id: tfcy
                                            width: 80
                                        }
                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Position Z (mm) :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CTextField {
                                            id: tfcz
                                            width: 80
                                        }
                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Appui :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CComboBox {
                                            id: appui
                                            model: ["Libre","Encastrement","DX", "DX DY","DX DY DZ","DX DY DZ DRX","DX DY DZ DRX DRY","DX DY DZ DRX DRZ","DX DY DZ DRY","DX DY DZ DRY DRZ", "DX DZ", "DY", "DY DRX DRZ","DY DZ","DY DZ DRX DRZ", "DZ"]
                                            width: 250
                                            height: 40
                                        }
                                    }
                                }
                                ButtonAdd{
                                    anchors.verticalCenter: parent.verticalCenter
                                    onClicked: {
                                        if (pageGeo.porte === 0){
                                            errorMessageNode.title = "Portée non définie"
                                            errorMessageNode.text = "Veuillez définir la portée avant de créer le modèle."
                                            errorMessageNode.visible = true
                                        }

                                        else{
                                            if (nodeModel.contain(tfcx.text,tfcy.text,tfcz.text)){
                                                errorMessageNode.title = "Doublon noeud"
                                                errorMessageNode.text = "Le noeud créé existe déjà."
                                                errorMessageNode.visible = true
                                            }
                                            else if (appui.currentText === ""){
                                                errorMessageNode.title = "Appui non défini"
                                                errorMessageNode.text = "Veuillez sélectionner un type d'appui"
                                                errorMessageNode.visible = true
                                            }
                                            else{
                                                nodeModel.append(tfcx.text, tfcy.text, tfcz.text, appui.currentText)
                                                tfcx.text = ""
                                                tfcy.text = ""
                                                tfcz.text = ""
                                                tfn1.text = ""
                                                tfn2.text = ""

                                                if (appui.currentText !== "Libre"){
                                                    appui.currentIndex = -1
                                                }
                                            }
                                        }
                                    }
                                }                                
                            }
                        }                       
                        Rectangle {
                            width: parent.width
                            height: 1
                            color: Theme.grey_3
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                        Rectangle {
                            color:"transparent"
                            height: 30 + nodeModel.count*30
                            width: parent.width
                            Column {
                                height: parent.height
                                width: parent.width
                                spacing: 10
                                Rectangle {
                                    id: nodeHeader
                                    color : "transparent"
                                    height: 30
                                    width: parent.width
                                    Row{
                                        spacing: 20
                                        width: parent.width
                                        Text {
                                            text: "N° noeud"
                                            font.bold: true
                                            color: Theme.grey_6
                                            width: 100
                                        }
                                        Text {
                                            text: "X (mm)"
                                            font.bold: true
                                            color: Theme.grey_6
                                            width: 120
                                        }
                                        Text {
                                            text: "Y (mm)"
                                            font.bold: true
                                            color: Theme.grey_6
                                            width: 120
                                        }
                                        Text {
                                            text: "Z (mm)"
                                            font.bold: true
                                            color: Theme.grey_6
                                            width: 120
                                        }
                                        Text {
                                            text: "Appui "
                                            font.bold: true
                                            color: Theme.grey_6
                                            width: 300
                                        }
                                    }
                                }
                                ListView{
                                    id: nodeListView
                                    objectName: "NodeListView"
                                    width: parent.width
                                    height: 20 + nodeModel.count*30
                                    model: nodeModel
                                    delegate: listDelegateNode
                                    onCountChanged: {
                                        nodeModule.height = 230 + nodeModel.count*30
                                        corps.height = 200 + nodeModule.height + beamModule.height
                                        pageGeo.node_list = nodeModel.get_ids()
                                        pageGeo.encas_node_list = nodeModel.get_encas()
                                    }
                                    ScrollIndicator.vertical: ScrollIndicator

                                }
                                MessageDialog {
                                    id: errorMessageNode
                                    title: "Doublon noeud"
                                    icon: StandardIcon.Critical
                                    text: "Le noeud créé existe déjà."
                                    standardButtons:  StandardButton.Abort
                                    onRejected: console.log("aborted")
                                    Component.onCompleted: visible = false
                                }
                            }
                        }
                    }
                }
                Rectangle{
                    height:25
                    color: "transparent"
                    width:50
                }
                Label {
                    text: "Profilés"
                    height: 30
                    anchors.left: parent.left
                    font.pixelSize: Theme.title_3
                    color: Theme.grey_6
                }
                Rectangle {
                    id: beamModule
                    border.color: Theme.grey_2
                    border.width: 1
                    radius: 4
                    width: corps.width - 60
                    state:"expanded"
                    states: [
                        State {
                            name: "expanded"
                            PropertyChanges { target: beamModule; height:230 + beamModel.count*30}
                        },
                        State {
                            name: "closed"
                            PropertyChanges { target: beamModule; height: 0;opacity:0;visible:false }
                            PropertyChanges { target: corps; height: 100 + nodeModule.height ;opacity:100;visible:true}
                        }
                    ]
                    transitions: [
                        Transition {
                            NumberAnimation {duration: 200;properties: "height"}
                            NumberAnimation {duration: 200;properties: "opacity"}
                            NumberAnimation {duration: 200;properties: "visible"}
                        }
                    ]
                    Column {
                        height: parent.height
                        width: parent.width - 40
                        anchors.left: parent.left
                        anchors.leftMargin: 20
                        anchors.top: parent.top
                        anchors.topMargin: 10
                        spacing: 10
                        Rectangle {
                            color : "transparent"
                            height: 35
                            width: parent.width
                            Row{
                                anchors.right: parent.right
                                anchors.rightMargin: 0
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                spacing: 5
                                Row {
                                    width: parent.width - 30
                                    height: parent.height
                                    spacing: 30
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Noeud 1 :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CTextField{
                                            id: tfn1
                                            width: 70
                                            validator:  RegExpValidator{regExp: /^[0-9][0-9]?$/}
                                        }                                        

                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Noeud 2 :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CTextField{
                                            id: tfn2
                                            width:70
                                            validator:  RegExpValidator{regExp: /^[0-9][0-9]?$/}
                                        }
                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Production :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CComboBox{
                                            id: production
                                            width: 140
                                            objectName: "ProductionCB"
                                        }
                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Matériau :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CComboBox{
                                            id: materiau
                                            width: 140
                                            objectName: "MaterialCB"
                                        }
                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Section :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CComboBox{
                                            id: section
                                            width: 120
                                            objectName: "SectionCB"
                                        }
                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Dimension :"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CComboBox{
                                            id: dimension
                                            width: 120
                                            objectName: "DimensionCB"
                                        }
                                        Label{
                                            text : "T :  " + pageGeo.temperature + "  °C"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                    }
                                    Row {
                                        spacing: 10
                                        Label{
                                            text : "Orientation (en °):"
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        CComboBox{
                                            id: combOr
                                            width: 50
                                            model: ["0","90","180","270"]
                                            onActivated: {
                                                if (tfn1.text ==="" || tfn2.text === ""){
                                                    errorMessageElem.title = "Noeuds de la barre non définis"
                                                    errorMessageElem.text = "Veuillez définir les noeuds avant de donner l'orientation"
                                                    errorMessageElem.visible = true
                                                }
                                                else{
                                                    if (!(tfn1.text  in pageGeo.node_list) || !(tfn1.text  in pageGeo.node_list)){
                                                        errorMessageElem.title = "Noeuds de la barre non définis"
                                                        errorMessageElem.text = "Veuillez choisir les noeuds déjà fini ou les créer"
                                                        errorMessageElem.visible = true
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                ButtonAdd{
                                    anchors.verticalCenter: parent.verticalCenter
                                    onClicked: {
                                        if ((pageGeo.temperature === 20) && (verifTemp == false)){
                                            warningMessage.visible = true
                                            verifTemp = true
                                        }
                                        else{
                                            if (tfn1.text === tfn2.text){
                                                errorMessageElem.title = "Noeuds identiques"
                                                errorMessageElem.text = "veuillez choisir deux noeuds disticnts pour créer une barre."
                                                errorMessageElem.visible = true
                                            }
                                            else{
                                                if (beamModel.check_node_beam(tfn1.text, tfn2.text,pageGeo.node_list)){
                                                    if (beamModel.contain(tfn1.text, tfn2.text)){
                                                        errorMessageElem.visible = true
                                                    }
                                                    else{
                                                        beamModel.append(tfn1.text, tfn2.text, production.currentText, materiau.currentText, section.currentText + ' ' + dimension.currentText, combOr.currentText,pageGeo.temperature)
                                                        tfn1.text = ""
                                                        tfn2.text = ""
                                                    }
                                                }
                                                else {
                                                    errorMessageElem.title = "Noeud inexistant"
                                                    errorMessageElem.text = "Les noeuds de la poutre n'ont pas été définis."
                                                    errorMessageElem.visible = true
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }                        
                        Rectangle {
                            width: parent.width
                            height: 1
                            color: Theme.grey_3
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                        Rectangle {
                            color:"transparent"
                            height: 100
                            width: parent.width
                            Row{
                                anchors.fill: parent
                                Rectangle{
                                    width: 200
                                    height: 150
                                    color: "transparent"
                                    Image{
                                        visible : tfn1.text ==="" || tfn2.text === "" || osup.printImage(tfn1.text, tfn2.text,section.currentText) === "None"
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreI.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text,section.currentText,combOr.currentText) === "XI" && (combOr.currentText === "0" || combOr.currentText === "180")
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreI_x_z.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "XI" && (combOr.currentText === "90" || combOr.currentText === "270")
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreI_x_y.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "YI" && (combOr.currentText === "0" || combOr.currentText === "180")
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreI_y_z.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "YI" && (combOr.currentText === "90" || combOr.currentText === "270")
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreI_y_x.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "ZI" && (combOr.currentText === "0" || combOr.currentText === "180")
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreI_z_x.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "ZI" && (combOr.currentText === "90" || combOr.currentText === "270")
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreU_z_y.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text,section.currentText,combOr.currentText) === "XU" && combOr.currentText === "0"
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreU_x_z.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "XU" && combOr.currentText === "90"
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreU_x_y.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "YU" && combOr.currentText === "0"
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreU_y_z.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "YU" && combOr.currentText === "90"
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreU_y_x.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText,combOr.currentText) === "ZU" && combOr.currentText === "0"
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreU_z_x.png"
                                    }
                                    Image{
                                        visible : tfn1.text !=="" && tfn2.text !== "" && osup.printImage(tfn1.text, tfn2.text, section.currentText, combOr.currentText) === "ZU" && combOr.currentText === "90"
                                        width:170
                                        height:120
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        source:"../../assets/images/poutreU_z_y.png"
                                    }
                                }                                
                                Rectangle{
                                    height : parent.height
                                    width : parent.width - 200
                                    Column {
                                        spacing: 10
                                        height: parent.height
                                        width: parent.width
                                        Rectangle {
                                            id: beamHeader
                                            color : "transparent"
                                            height: 30
                                            width: parent.width
                                            Row{
                                                spacing: 20
                                                width: parent.width
                                                Text {
                                                    text: "N° profilé"
                                                    font.bold: true
                                                    color: Theme.grey_6
                                                    width: 100
                                                }
                                                Text {
                                                    text: "Noeud 1"
                                                    font.bold: true
                                                    color: Theme.grey_6
                                                    width: 100
                                                }
                                                Text {
                                                    text: "Noeud 2"
                                                    font.bold: true
                                                    color: Theme.grey_6
                                                    width: 100
                                                }
                                                Text {
                                                    text: "Production"
                                                    font.bold: true
                                                    color: Theme.grey_6
                                                    width: 200
                                                }
                                                Text {
                                                    text: "Matériaux"
                                                    font.bold: true
                                                    color: Theme.grey_6
                                                    width: 200
                                                }
                                                Text {
                                                    text: "Section"
                                                    font.bold: true
                                                    color: Theme.grey_6
                                                    width: 200
                                                }
                                                Text {
                                                    text: "Orientation"
                                                    font.bold: true
                                                    color: Theme.grey_6
                                                    width: 200
                                                }
                                            }
                                        }
                                        ListView{
                                            id: beamListView
                                            objectName: "BeamListView"
                                            width: parent.width
                                            height: 20 + beamModel.count*30
                                            model: beamModel
                                            delegate: listDelegateBeam
                                            onCountChanged: {
                                                beamModule.height = 230 + beamModel.count*30
                                                corps.height = 200 + nodeModule.height + beamModule.height
                                                pageGeo.beam_list = beamModel.get_ids()
                                            }
                                            ScrollIndicator.vertical: ScrollIndicator { }
                                        }
                                        Rectangle {
                                            anchors.right: parent.right
                                            height: 100
                                            width: 140
                                            color: "transparent"
                                            ButtonText {
                                                anchors.left: parent.left
                                                anchors.verticalCenter: parent.verticalCenter
                                                text: "Vérifier la géométrie"
                                                color: Theme.grey_3
                                                width: 130
                                                onClicked:{
                                                    osup.create_file("geo_display")
                                                    osup.open_file_gmsh()
                                                }
                                            }
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
                                        MessageDialog {
                                            id: warningMessage
                                            title: "Température non défini"
                                            icon: StandardIcon.Warning
                                            text : "Aucune valeur de température n'a été renseigné, si la valeur de température
prise est la valeur par défaut (20°C) veuillez ignorer ce message. Sinon
veuillez modifier la valeur dans l'étape 1: Définition des conditions de calcul."
                                            standardButtons: StandardButton.Yes | StandardButton.Cancel
                                            Component.onCompleted: visible = false
                                            onYes: {
                                                verifTemp = true
                                                if (tfn1.text === tfn2.text){
                                                    errorMessageElem.title = "Noeuds identiques"
                                                    errorMessageElem.text = "veuillez choisir deux noeuds disticnts pour créer une barre."
                                                    errorMessageElem.visible = true
                                                }
                                                else{
                                                    if (beamModel.check_node_beam(tfn1.text, tfn2.text,pageGeo.node_list)){
                                                        if (beamModel.contain(tfn1.text, tfn2.text)){
                                                            errorMessageElem.visible = true
                                                        }
                                                        else{
                                                            beamModel.append(tfn1.text, tfn2.text, production.currentText, materiau.currentText, section.currentText + ' ' + dimension.currentText, combOr.currentText,pageGeo.temperature)
                                                            tfn1.text = ""
                                                            tfn2.text = ""
                                                        }
                                                    }
                                                    else {
                                                        errorMessageElem.title = "Noeud inexistant"
                                                        errorMessageElem.text = "Les noeuds de la poutre n'ont pas été définis."
                                                        errorMessageElem.visible = true
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

        }
    }
    //--------------------------------------------------------------------------------------
    //MODULE VIDE :FIN D'INSERTION DE CODE
}

