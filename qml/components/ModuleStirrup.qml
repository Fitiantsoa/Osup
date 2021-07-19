import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import QtQuick.Dialogs 1.1

import StirrupListModel 1.0

import "../theme.js" as Theme
import "../base"
import "../ui"

Rectangle {
    id: osupModuleEtrier
    width: parent.width
    height: title.height+corps.height
    color:"transparent"
    property alias l: textfieldL.text
    property alias dn: textfieldD.text
    property alias t: textfieldt.text
    property alias htmlEtrier: maListEtrier

    Rectangle {
        id:title
        width: parent.width
        height:  25
        color: "transparent"
        anchors.top: parent.top
        anchors.topMargin: 40
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
            Label{
                id:moduletitle
                text:"Etape 4 : Etrier / Collier"
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
                PropertyChanges { target: corps; height: titreRect.height + rectModel.height}
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
                NumberAnimation {duration: 50;properties: "opacity"}
                NumberAnimation {duration: 50;properties: "visible"}
            }
        ]
        Column{
            anchors.fill:parent
            spacing: 5
            Rectangle{
                id : titreRect
                width : parent.width
                height :pageGeo.rccm.checked ?375 : 475
                color: "transparent"
                Row{
                    anchors.fill: parent
                    Rectangle{
                        id: rectDroite
                        width: parent.width/3
                        height: parent.height
                        color: "transparent"
                        Image{
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                            source:pageGeo.rccm.checked ? "../../assets/images/Etrier_RCCM.PNG" : "../../assets/images/Etrier_EN.PNG"
                        }
                    }
                    Rectangle {
                        id: separationGauche
                        color: Theme.grey_2
                        width: 1
                        anchors.top: parent.top
                        anchors.topMargin: 30
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 30
                    }
                    Rectangle{
                        id: rectGauchee
                        width: parent.width*2/3
                        height: parent.height
                        color: "transparent"
                        Column{
                            id: column
                            anchors.fill: parent
                            anchors.topMargin: 30
                            anchors.rightMargin: 20
                            anchors.leftMargin: 20
                            spacing : 10
                            Rectangle{
                                height : 40
                                width : parent.width
                                Column{
                                    anchors.fill: parent
                                    spacing: 30
                                    Rectangle{
                                        height : 25
                                        width : parent.width
                                        RowLayout{
                                            anchors.fill: parent
                                            spacing :pageGeo.rccm.checked ? parent.width/20 : parent.width/20
                                            RowLayout{
                                                spacing:10
                                                height : parent.height
                                                Label{
                                                    Layout.preferredWidth: 90
                                                    text : "Nom de l'étrier :"
                                                    color : Theme.grey_6
                                                }
                                                CTextField{
                                                    id : nomEtrier
                                                    Layout.fillWidth: true
                                                }
                                            }
                                            RowLayout{
                                                spacing:10
                                                height : parent.height
                                                Label{
                                                    Layout.preferredWidth: 30
                                                    text : "Tuyau :"
                                                    color : Theme.grey_6
                                                }
                                                CComboBox{
                                                    Layout.fillWidth: true
                                                    objectName: "BoltCB"
                                                    id: boulonCombox
                                                }
                                            }
                                            RowLayout{
                                                spacing:10
                                                height : parent.height
                                                enabled:pageGeo.rccm.checked
                                                visible : enabled
                                                Label{
                                                    Layout.preferredWidth: 100
                                                    text : "Materiaux du boulon :"
                                                    color : Theme.grey_6
                                                }
                                                CComboBox{
                                                    Layout.fillWidth: true
                                                    id: materiauxCombobox
                                                    model : ["Ferritique", "Austénitique"]
                                                }
                                            }
                                            RowLayout{
                                                spacing:10
                                                height : parent.height
                                                Label{
                                                    Layout.preferredWidth: 90
                                                    text : "Profilés associé :"
                                                    color : Theme.grey_6
                                                }
                                                CComboBox{
                                                    id : profileAssocie
                                                    Layout.fillWidth: true
                                                    model : pageGeo.beam_list
                                                    onCurrentTextChanged: {
                                                        osup.update_stirrup_thickness(profileAssocie.currentText, twtfCbbx.currentText)
                                                    }
                                                }
                                            }
                                            RowLayout{
                                                spacing:5
                                                height : parent.height
                                                width : 200
                                                enabled: !pageGeo.rccm.checked
                                                visible : enabled
                                                Label{
                                                    Layout.preferredWidth: 120
                                                    text : " Plan de cisaillement
dans la partie du boulon: "
                                                    color : Theme.grey_6
                                                }
                                                CComboBox{
                                                    Layout.fillWidth: true
                                                    id: planCombobox
                                                    model : ["Non filetée", "Filetée"]
                                                }
                                            }
                                            RowLayout{
                                                spacing:5
                                                height : parent.height
                                                width : 170
                                                enabled: !pageGeo.rccm.checked
                                                visible : enabled
                                                Label{
                                                    Layout.preferredWidth: 80
                                                    text : "Tête du boulon :"
                                                    color : Theme.grey_6
                                                }
                                                CComboBox{
                                                    Layout.fillWidth: true
                                                    id: fraiseCombobox
                                                    model : ["Non fraisé", "Fraisé"]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            Rectangle {
                                height : 25
                                width : parent.width
                                color : "transparent"
                                RowLayout{
                                    anchors.fill :parent
                                    spacing : 30
                                    Label{
                                        id: titreGeo
                                        font.bold: true
                                        color : Theme.grey_6
                                        text:"Caractéristiques Géométriques :"
                                    }
                                }
                            }
                            Rectangle {
                                height : 25
                                width : parent.width
                                color : "transparent"
                                Row{
                                    spacing :30
                                    anchors.fill: parent
                                    RowLayout{
                                        spacing:10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text :pageGeo.rccm.checked ? "Section réelle du noyau
du boulon (mm²) : " : "Aire résistante en traction
du boulon (mm²)   "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label {
                                            Layout.preferredWidth: 40
                                            width : parent/8
                                            id: labelSb
                                            font.bold: true
                                            color : Theme.primary
                                            text:pageGeo.rccm.checked ? "S  " : "A   "
                                            Label {
                                                font.bold: true
                                                color : Theme.primary
                                                text:pageGeo.rccm.checked ? "B  = " : "s  = "
                                                x:6
                                                y:4
                                            }
                                        }
                                        CTextField{
                                            id: textfieldAs
                                            enabled: false
                                            visible : !pageGeo.rccm.checked
                                            objectName: "AsTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                            opacity: 1

                                        }
                                        CTextField{
                                            id: textfieldSb
                                            enabled: false
                                            visible :pageGeo.rccm.checked
                                            objectName: "SbTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                            opacity: 1
                                        }
                                    }
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        enabled: !pageGeo.rccm.checked
                                        visible : enabled
                                        Label{
                                            text : planCombobox.currentText==="Non filetée" ? "Section transversale
brute du boulon (mm²) :" : "Aire de la section
nette du boulon (mm²)"
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label {
                                            Layout.preferredWidth: 40
                                            width : parent/8
                                            id: labelA
                                            font.bold: true
                                            color : Theme.primary
                                            text: qsTr("A  =")

                                        }
                                        CTextField{
                                            id: textfieldA
                                            enabled: false
                                            objectName: "ATF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                            opacity: 1

                                        }
                                    }

                                }
                            }
                            Rectangle {
                                height : 25
                                width : parent.width
                                color : "transparent"
                                Row{
                                    anchors.fill: parent
                                    spacing : 30
                                    RowLayout{
                                        spacing:10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text : "Diamètre nominal du
boulon (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            Layout.preferredWidth: 40
                                            id: lableD
                                            text:"d    ="
                                            font.bold: true
                                            color : Theme.primary
                                        }
                                        CTextField{
                                            id: textfieldD
                                            objectName: "dTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                            enabled: false
                                        }
                                    }
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        enabled: !pageGeo.rccm.checked
                                        visible : enabled
                                        Label{
                                            text : "Diamètre moyen (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            Layout.preferredWidth: 45
                                            id: lableDm
                                            text:"d  "
                                            font.bold: true
                                            color : Theme.primary
                                            Label {
                                                font.bold: true
                                                color : Theme.primary
                                                text: "m  = "
                                                x:6
                                                y:4
                                            }
                                        }
                                        CTextField{
                                            id: textfieldDm
                                            enabled: false
                                            objectName: "dmTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                            opacity: 1
                                        }
                                    }
                                }
                            }
                            Rectangle {
                                height : 25
                                width : parent.width
                                color : "transparent"
                                Row{
                                    anchors.fill: parent
                                    spacing : 30
                                    RowLayout{
                                        spacing:10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text : "Pas gros du boulon (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            Layout.preferredWidth: 40
                                            id: lablePas
                                            text:"Pas = "
                                            font.bold: true
                                            color : Theme.primary
                                        }
                                        CTextField{
                                            id: textfieldPas
                                            objectName: "pasTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                            enabled: false
                                            opacity: 1
                                        }
                                    }
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        enabled: !pageGeo.rccm.checked
                                        visible : enabled
                                        Label{
                                            text : "Diamètre nominal des
trous (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            Layout.preferredWidth: 45
                                            id: lableDo
                                            text:"d  "
                                            font.bold: true
                                            color : Theme.primary
                                            Label {
                                                font.bold: true
                                                color : Theme.primary
                                                text: "o  = "
                                                x:6
                                                y:4
                                            }
                                        }
                                        CTextField{
                                            id: textfieldDo
                                            enabled: false
                                            objectName: "doTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                            opacity: 1
                                        }
                                    }
                                }
                            }
                            Rectangle {
                                height : 25
                                width : parent.width
                                color : "transparent"
                                Row{
                                    anchors.fill: parent
                                    spacing : 30
                                    RowLayout{
                                        spacing:10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text :pageGeo.rccm.checked ? "Epaisseur du
matériau assemblé (mm) : " : "Epaisseur de la pièce attachée
extérieure la plus mince (mm) "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            id: lablet
                                            text:"t  ="
                                            font.bold: true
                                            color : Theme.primary
                                        }
                                        CComboBox{
                                            id: twtfCbbx
                                            Layout.preferredWidth: 50
                                            model:ListModel {
                                                id: etrItem
                                                ListElement {text: "tf"}
                                                ListElement {text: "tw"}
                                            }
                                            onCurrentTextChanged: {
                                                osup.update_stirrup_thickness(profileAssocie.currentText, twtfCbbx.currentText)
                                            }
                                        }
                                        CTextField{
                                            id: textfieldt
                                            objectName: "tTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}

                                        }
                                    }
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        enabled: !pageGeo.rccm.checked
                                        visible : enabled
                                        Label{
                                            text : "Epaisseur de la plaque sous
la tête ou l'écrou (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            id: labletp
                                            text:"t  "
                                            font.bold: true
                                            color : Theme.primary
                                            Label {
                                                font.bold: true
                                                color : Theme.primary
                                                text: "p = "
                                                x:6
                                                y:4
                                            }
                                        }
                                        CTextField{
                                            id: textfieldtp
//                                            objectName: "tpTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}

                                        }
                                    }
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        enabled:pageGeo.rccm.checked
                                        visible : enabled
                                        Label{
                                            text : "Distance minimale boulon/
bord libre (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            Layout.preferredWidth: 40
                                            id: lableL
                                            text:"l  = "
                                            font.bold: true
                                            color : Theme.primary
                                        }
                                        CTextField{
                                            id: textfieldL
//                                            objectName: "lTF"
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                        }
                                    }
                                }
                            }
                            Rectangle {
                                height : 25
                                width : parent.width
                                color : "transparent"
                                enabled: !pageGeo.rccm.checked
                                visible : enabled
                                Row{
                                    anchors.fill: parent
                                    spacing : 30
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text :"Pince longitudinale (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            id: lablee1
                                            text:"e  "
                                            font.bold: true
                                            color : Theme.primary
                                            Label {
                                                font.bold: true
                                                color : Theme.primary
                                                text: "1 = "
                                                x:6
                                                y:4
                                            }
                                        }
                                        CTextField{
                                            id: textfielde1
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}

                                        }
                                    }
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text : "Pince transversale (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            id: lablee2
                                            text:"e "
                                            font.bold: true
                                            color : Theme.primary
                                            Label {
                                                font.bold: true
                                                color : Theme.primary
                                                text: "2 = "
                                                x:6
                                                y:4
                                            }
                                        }
                                        CTextField{
                                            id: textfielde2
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                        }
                                    }
                                }
                            }
                            Rectangle {
                                height : 25
                                width : parent.width
                                color : "transparent"
                                enabled: !pageGeo.rccm.checked
                                visible : enabled
                                Row{
                                    anchors.fill: parent
                                    spacing : 30
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text :"Entraxe longitudinale (mm) : "
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            id: lablep1
                                            text:"p  "
                                            font.bold: true
                                            color : Theme.primary
                                            Label {
                                                font.bold: true
                                                color : Theme.primary
                                                text: "1 = "
                                                x:6
                                                y:4
                                            }
                                        }
                                        CTextField{
                                            id: textfieldp1
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                        }
                                    }
                                }
                            }
                            Rectangle {
                                height : 15
                                width : parent.width
                                color : "transparent"
                            }
                            Rectangle {
                                height : 10
                                width : parent.width
                                color : "transparent"
                                RowLayout{
                                    anchors.fill : parent
                                    spacing : 30
                                    Label {
                                        text: qsTr("Données Matériaux :")
                                        color : Theme.grey_6
                                        font.bold: true
                                    }
                                }
                            }
                            Rectangle {
                                height : 25
                                width :parent.width
                                color : "transparent"
                                Row{
                                    anchors.fill: parent
                                    spacing : 30
                                    RowLayout{
                                        spacing:10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text : "Limite élastique (MPa) :"
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            id: lableSy
                                            text:pageGeo.rccm.checked ? "Sy = " : "fy = "
                                            font.bold: true
                                            color : Theme.primary
                                        }
                                        CTextField{
                                            objectName: "Sy"
                                            id: textfieldSy
                                            enabled: pageGeo.rccm.checked
                                            visible : enabled
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}

                                        }
                                        CTextField{
                                            id: textfieldfy
                                            enabled: ! pageGeo.rccm.checked
                                            visible : enabled
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                        }
                                    }
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text : "Résistance à la traction (MPa) :"
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label{
                                            id: lableSu
                                            text: pageGeo.rccm.checked ? "Su = " : "fu = "
                                            font.bold: true
                                            color : Theme.primary
                                        }
                                        CTextField{
                                            id: textfieldSu
                                            enabled: pageGeo.rccm.checked
                                            visible : enabled
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}

                                        }
                                        CTextField{
                                            id: textfieldfu
                                            enabled: ! pageGeo.rccm.checked
                                            visible : enabled
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                        }
                                    }

                                }
                            }
                            Rectangle {
                                enabled: ! pageGeo.rccm.checked
                                visible : enabled
                                height : 25
                                width :parent.width
                                color : "transparent"
                                Row{
                                    anchors.fill: parent
                                    spacing : 30
                                    RowLayout{
                                        spacing: 10
                                        height : parent.height
                                        width : (parent.width-50)/2
                                        Label{
                                            text : "Résistance ultime à la
traction du boulon (MPa) :"
                                            Layout.preferredWidth: 160
                                            color : Theme.grey_6
                                        }
                                        Label {
                                            Layout.preferredWidth: 40
                                            width : parent/8
                                            id: labelFub
                                            font.bold: true
                                            color : Theme.primary
                                            text: qsTr("F ")
                                            Label {
                                                font.bold: true
                                                color : Theme.primary
                                                text: "ub  = "
                                                x:6
                                                y:4
                                            }
                                        }
                                        CTextField{
                                            id: textfieldFub
                                            validator: RegExpValidator { regExp: /^[-+]?[0-9]*\.?[0-9]+/}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            ButtonAdd{
                anchors.right: parent.right
                anchors.margins: 30
                onClicked: {
                    if (! maListEtrier.contain(nomEtrier.text) && nomEtrier.text !== "") {
                        if (textfieldL.text === "" || textfieldSu.text === "" || textfieldSy.text ==="" ){
                            errorMessageStirrup.title = "Erreur valeur"
                            errorMessageStirrup.text = "Veuillez renseigner toutes les valeurs"
                            errorMessageStirrup.open()
                        }
                        else{
                        osup.append_stirrup(nomEtrier.text,
                                            materiauxCombobox.currentText,
                                            textfieldSb.text,
                                            textfieldAs.text,
                                            textfieldD.text,
                                            textfieldL.text,
                                            textfieldt.text,
                                            textfieldPas.text,
                                            textfieldSy.text,
                                            textfieldfy.text,
                                            textfieldSu.text,
                                            textfieldfu.text,
                                            textfieldFub.text,
                                            textfieldA.text,
                                            textfieldDm.text,
                                            textfieldDo.text,
                                            textfieldtp.text,
                                            planCombobox.currentText,
                                            fraiseCombobox.currentText,
                                            textfieldp1.text,
                                            textfielde1.text,
                                            textfielde2.text);
                       }
                    }
                    else {
                        errorMessageStirrup.title = "Erreur"
                        errorMessageStirrup.text = "Veuillez entrer un autre nom pour l'étrier"
                        errorMessageStirrup.open()
                    }
                }
            }
            Rectangle{
                id : rectModel
                height : 100 + 30*maListView.count
                width : corps.width
                color : "transparent"
                Column{
                    anchors.fill: parent
                    spacing : 5
                    Rectangle{
                        height : 1
                        anchors.horizontalCenter: parent.horizontalCenter
                        width : parent.width - 60
                        color : Theme.grey_2
                    }
                    Rectangle{
                        height :30
                        width : parent.width
                        color: "transparent"
                        Row{
                            anchors.fill: parent
                            Rectangle{
                                width : parent.width/5
                                height : parent.height
                                color: "transparent"
                                Label{
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    font.bold: true
                                    color : Theme.grey_6
                                    text : "Nom de l'étrier"
                                }
                            }
                            Rectangle{
                                width : parent.width/4
                                height : parent.height
                                color: "transparent"
                                Label{
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    font.bold: true
                                    color : Theme.grey_6
                                    text : "Caractéristiques Géométriques"
                                }
                            }
                            Rectangle{
                                width : parent.width/5
                                height : parent.height
                                color: "transparent"
                                Label{
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    font.bold: true
                                    color : Theme.grey_6
                                    text : "Données Matériaux"
                                }
                            }
                            Rectangle{
                                width : parent.width/5
                                height : parent.height
                                color: "transparent"
                                Label{
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    font.bold: true
                                    color : Theme.grey_6
                                    text : "Contraintes Admissibles"
                                }
                            }
                        }
                    }
                    StirrupListModel{
                        id : maListEtrier
                    }
                    Component{
                        id : monDelegue
                        Item{
                            id: item1
                            width: parent.width
                            height:100
                            clip: true
                            Rectangle{
                                anchors.fill: parent
                                color : "transparent"
                                Row{
                                    anchors.fill: parent
                                    Rectangle{
                                        width : parent.width/5
                                        height : parent.height
                                        color : "transparent"
                                        Label{
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            color : Theme.grey_6
                                            text : nom
                                            font.bold: true
                                        }
                                    }
                                    Rectangle{
                                        height : parent.height -10
                                        anchors.verticalCenter: parent.verticalCenter
                                        width : 1
                                        color : Theme.grey_2
                                    }
                                    Rectangle{
                                        height : parent.height
                                        width : parent.width/4
                                        color : "transparent"
                                        Column{
                                            width: parent.width
                                            height: parent.height/2
                                            Row {
                                                anchors.fill: parent
                                                anchors.leftMargin: 15
                                                anchors.topMargin: 6
                                                width: parent.width
                                                height: parent.height/2
                                                Rectangle {
                                                    height: parent.height
                                                    width: parent.width/2
                                                    color: "transparent"
                                                    Column{
                                                        width: parent.width
                                                        height: parent.height/2
                                                        Label{
                                                            Layout.preferredWidth: 5
                                                            text : DN
                                                            color : Theme.grey_6
                                                            font.bold : true
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "A (mm²) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : A
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "d (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : d
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "t (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : t
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            visible: ! pageGeo.rccm.checked
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "P1 (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : P1
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            visible: ! pageGeo.rccm.checked
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "e1 (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : e1
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                    }
                                                }
                                                Rectangle{
                                                    height: parent.height
                                                    width: parent.width/2
                                                    color: "transparent"
                                                    Column{
                                                        width: parent.width
                                                        height: parent.height/2
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : ! pageGeo.rccm.checked?"As (mm²) =":"Sb (mm²) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : ! pageGeo.rccm.checked?As:Sb
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "Pas (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : pas
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            visible: ! pageGeo.rccm.checked
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text :  "dm (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text :  dm
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            visible: ! pageGeo.rccm.checked
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text :  "do (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : Do
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text :  ! pageGeo.rccm.checked?"tp (mm) =":"l (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text :  ! pageGeo.rccm.checked?tp:l
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            visible: ! pageGeo.rccm.checked
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text :  "e2 (mm) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : e2
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    Rectangle{
                                        height : parent.height -10
                                        anchors.verticalCenter: parent.verticalCenter
                                        width : 1
                                        color : Theme.grey_2

                                    }
                                    Rectangle{
                                        height : parent.height
                                        width : parent.width/5
                                        color : "transparent"
                                        Row{
                                            anchors.fill: parent
                                            anchors.leftMargin: 15
                                            anchors.topMargin: 3
                                            Rectangle{
                                                height : parent.height
                                                anchors.verticalCenter: parent.verticalCenter
                                                width : parent.width
                                                Column{
                                                    anchors.fill: parent
                                                    Rectangle{
                                                        width :parent.width
                                                        height : parent.height/6
                                                        color : "transparent"
                                                        RowLayout{
                                                            anchors.topMargin: 5
                                                            anchors.fill : parent
                                                            Label{
                                                                Layout.preferredWidth : 5
                                                                text : ! pageGeo.rccm.checked?"fy (Mpa) =":"Sy (Mpa) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                Layout.preferredWidth: 0
                                                                text : ! pageGeo.rccm.checked?fy:Sy
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                    }

                                                    Rectangle{
                                                        width :parent.width
                                                        height : parent.height/6
                                                        color : "transparent"
                                                        RowLayout{
                                                            anchors.topMargin: 5
                                                            anchors.fill : parent
                                                            Label{
                                                                Layout.preferredWidth : 5
                                                                text :! pageGeo.rccm.checked?"fu (Mpa) =":"Su (MPa) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                Layout.preferredWidth: 0
                                                                text : ! pageGeo.rccm.checked?fu:Su
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                    }
                                                    Rectangle{
                                                        width :parent.width
                                                        height : parent.height/6
                                                        color : "transparent"
                                                        RowLayout{
                                                            anchors.topMargin: 5
                                                            anchors.fill : parent
                                                            Label{
                                                                Layout.preferredWidth : 5
                                                                text : ! pageGeo.rccm.checked?"Fub (Mpa) =":""
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                Layout.preferredWidth: 0
                                                                text : Fub
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                    }

                                                }
                                            }
                                        }
                                    }
                                    Rectangle{
                                        height : parent.height -10
                                        anchors.verticalCenter: parent.verticalCenter
                                        width : 1
                                        color : Theme.grey_2

                                    }
                                    Rectangle{
                                        height : parent.height
                                        width : parent.width/4
                                        color : "transparent"
                                        Column{
                                            width: parent.width
                                            height: parent.height/2
                                            Row {
                                                anchors.fill: parent
                                                anchors.leftMargin: 15
                                                anchors.topMargin: 6
                                                width: parent.width
                                                height: parent.height/2
                                                Rectangle {
                                                    height: parent.height
                                                    width: parent.width/2
                                                    color: "transparent"
                                                    Column{
                                                        width: parent.width
                                                        height: parent.height/2
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "Ft (Mpa) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : Ft
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : ! pageGeo.rccm.checked?"Bp (Mpa) =":"Fp (Mpa) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : ! pageGeo.rccm.checked?Bp:Fp
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                    }
                                                }
                                                Rectangle{
                                                    height: parent.height
                                                    width: parent.width/2
                                                    color: "transparent"
                                                    Column{
                                                        width: parent.width
                                                        height: parent.height/2
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "Fv (Mpa) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : Fv
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                        Row{
                                                            width: parent.width
                                                            height: parent.height/2
                                                            visible: ! pageGeo.rccm.checked
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : "Fb (Mpa) ="
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                            Label{
                                                                width: parent.width/2
                                                                height: parent.height
                                                                text : Fb
                                                                color : Theme.grey_6
                                                                font.bold : true
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                ButtonTable{
                                    id: removeButton
                                    text: "\uE808"
                                    font.family: "fontello"
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.right: parent.right
                                    anchors.rightMargin: 15
                                    onClicked: {
                                        osup.remove_stirrup(maListEtrier.get_name(index))
                                        maListEtrier.remove(index);
                                    }
                                }
                            }
                        }
                    }
                    Rectangle{
                        id : rectaaaang
                        width : parent.width
                        height: 50+30*maListView.count
                        color: "transparent"
                        ListView{
                            id: maListView
                            objectName: "ListViewStirrup"
                            anchors.fill:parent
                            contentHeight: 20
                            interactive: false
                            delegate: monDelegue
                            model: maListEtrier
                            focus:true
                            onCountChanged: {
                                rectModel.height = 80+120*maListView.count
                            }
                        }
                    }
                }
            }
        }
    }

    MessageDialog {
        id: errorMessageStirrup
        icon: StandardIcon.Critical
        standardButtons:  StandardButton.Abort
        onRejected: console.log("aborted")
        Component.onCompleted: visible = false
    }
}


