import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import QtQuick.Dialogs 1.1


import "../components"
import "../theme.js" as Theme
import "../base"
import "../ui"

Rectangle {
    id: osupModuleNorme
    width: parent.width
    height: title.height+corps.height
    color:"transparent"
//    property alias temperature: textfieldTemperature.text
//    property alias lvlA_check: lvlA.checked
//    property alias lvlC_check: lvlC.checked
//    property alias lvlD_check: lvlD.checked
    property alias rccm : rccm
    property alias lvlA : lvlA
//    property alias en_check : normeRadioButtonEN.checked

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
                text:"Etape 1 : Définition des conditions de calcul"
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
                PropertyChanges { target: corps; height: 250}
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
                        spacing: 5
                        Rectangle{
                            height : 30
                            anchors.left: parent.left
                            anchors.right: parent.right
                            RowLayout{
                                anchors.fill: parent
                                Label{
                                    Layout.preferredWidth: 100
                                    text : "Réglementation :"
                                    color : Theme.grey_6
                                }
                                CRadioButton{
                                    id: rccm
                                    objectName: "RccmRB"
                                    text:"RCC-M"
                                    checked:true
                                }
                                CRadioButton{
                                    id: en
                                    objectName: "EnRB"
                                    text:"EN 13480-3"
                                    checked:false
                                }
                            }
                        }
                        Rectangle{
                            height : 70
                            anchors.left: parent.left
                            anchors.right: parent.right
                            RowLayout{
                                anchors.fill: parent
                                Label{
                                    Layout.preferredWidth: 100
                                    text : "Niveau :"
                                    anchors.top: parent.top
                                    color : Theme.grey_6
                                }
                                Rectangle{
                                    Layout.fillWidth: true
                                    height : parent.height
                                    ColumnLayout{
                                        enabled: true
                                        visible : rccm.checked
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        CRadioButton{
                                            objectName: "NivOABRB"
                                            id:lvlA
                                            text: "Niveau OAB"
                                            checked: true
                                        }
                                        CRadioButton{
                                            id:lvlC
                                            objectName: "NivCRB"
                                            text: "Niveau C"
                                            checked: false
                                        }
                                        CRadioButton{
                                            id:lvlD
                                            objectName: "NivDRB"
                                            text: "Niveau D"
                                            checked: false
                                        }
                                    }
                                    ColumnLayout{
                                        enabled: false
                                        visible : ! rccm.checked
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        CRadioButton{
                                            objectName: "NivNormalRB"
                                            id:lvlN
                                            text: "Normal"
                                            checked: true
                                        }
                                        CRadioButton{
                                            id:lvlO
                                            objectName: "NivOccRB"
                                            text: "Occasionnel"
                                            checked: false
                                        }
                                     }
                                }
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
//                Rectangle{
//                    height : parent.height
//                    width : 230
//                    Row{
//                        anchors.fill: parent
//                        spacing: 0
//                        Rectangle{
//                            height : 20
//                            width : parent.width/4
//                            RowLayout{
//                                anchors.top: parent.top
//                                anchors.bottom: parent.bottom
//                                anchors.right: parent.right
//                                anchors.left: parent.left
//                                anchors.leftMargin: 15
//                                Label{
//                                    Layout.preferredWidth: 100
//                                    text : "Repère :"
//                                    color : Theme.grey_6
//                                }
//                            }
//                        }
//                        Rectangle{
//                            height : parent.height
//                            width : 150
//                            Image {
//                                source: "./images/repère.PNG"
//                                anchors.fill: parent
//                            }
//                        }
//                    }
//                }
//                Rectangle{
//                    id: separateur
//                    color: Theme.grey_3
//                    anchors.verticalCenter: parent.verticalCenter
//                    width: 1
//                    height: parent.height-10
//                }
                Rectangle{
                    height : parent.height
                    width : ((parent.width-150)/2) - 25
                    id : table
                    Column{
                        anchors.fill: parent
                        anchors.margins: 5
                        spacing: -1
                        RowLayout{
                            spacing: 15
                            anchors.right: parent.right
                            anchors.left: parent.left
                            anchors.leftMargin: 15
                            anchors.rightMargin: 20
                            Label{
                                id: labelTemperature
                                text: "Température de calcul:"
                                Layout.preferredWidth: 110
                                color : Theme.grey_6
                            }
                            CTextField{
                                id: textfieldTemperature
//                                enabled: false
                                opacity: enabled?1:0.6
                                objectName: "CalculationTemperatureTF"
                                placeholderText: qsTr("Par défaut 20")
                                Layout.preferredWidth: 150
                                validator: IntValidator{}
                                function minmax(temperature) {
                                    if (temperature < 20) {
                                        return 20
                                    }
                                    else if (temperature > 300) {
                                        return 300
                                    }
                                    return temperature
                                }
//                                onTextChanged: {
//                                    Osup.setCgenerale(textfieldTemperature.text)
//                                }
                                onFocusChanged: {
                                    textfieldTemperature.text = minmax(textfieldTemperature.text)
                                    pageGeo.temperature = textfieldTemperature.text
                                    osup.changeTemperature(textfieldTemperature.text)
//                                    Osup.majMatPlat()
//                                    Osup.majMatProf()
                                }
                                Keys.onEnterPressed:{
                                    textfieldTemperature.text = minmax(textfieldTemperature.text)
                                    pageGeo.temperature = textfieldTemperature.text
                                    osup.changeTemperature(textfieldTemperature.text)
                                }
                            }
                            Label {
                                visible: true
                                text: "°C"
                                color:  Theme.grey_6
                                Layout.preferredWidth: 10
                                anchors.verticalCenter: parent.verticalCenter
                            }
                            Label{
                                text : "Température ambiante :"
                                Layout.preferredWidth: 110
                                color : Theme.grey_6
                            }
                            Label{
                                objectName: "newTemperature"
                                text : "20°C"
                                anchors.rightMargin: parent.right
                                Layout.preferredWidth: 10
                                font.bold: true
                                color : Theme.primary
                                visible : text!=""
                            }
                        }
                        RowLayout{
                            spacing: 15
                            anchors.right: parent.right
                            anchors.left: parent.left
                            anchors.leftMargin: 15
                            anchors.rightMargin: 20
                            Label{
                                id: labelCoeff
                                text: "Coefficient de frottement:"
                                Layout.preferredWidth: 130
                                color : Theme.grey_6
                            }
                            CTextField{
                                id: textfieldCoeff
                                Layout.preferredWidth: 150
                                validator: RegExpValidator{regExp: /^[0]{0,1}[.][0-9]{0,1}([0-9]{0,1})?([0-9]{0,1})?/}
                                opacity: enabled?1:0.6
                                objectName: "FrictionCoefficientTF"
                                text: "0.3"
//                                onEditingFinished: {
//                                    Osup.majMatPlat()
//                                    Osup.majMatProf()
//                                }
//                                onTextChanged: {
//                                    Osup.setCgeneraleF(textfieldCoeff.text)
//                                }
                            }
                        }
                        RowLayout{
                            spacing: 15
                            anchors.right: parent.right
                            anchors.left: parent.left
                            anchors.leftMargin: 15
                            anchors.rightMargin: 20
                            Label{
                                id: labelRatioProf
                                text: "Ratio max profilé:"
                                Layout.preferredWidth: 130
                                color : Theme.grey_6
                            }
                            CTextField{
                                id: ratioProf
                                text: "1"
                                Layout.preferredWidth: 150
                                validator: RegExpValidator{regExp: /^[0-1]{0,1}[.][0-9]{0,1}([0-9]{0,1})?([0-9]{0,1})?/}
                                opacity: enabled?1:0.6
                                objectName: "RatioMaxProf"

                            }
                        }
                        RowLayout{
                            spacing: 15
                            anchors.right: parent.right
                            anchors.left: parent.left
                            anchors.leftMargin: 15
                            anchors.rightMargin: 20
                            Label{
                                id: labelRatioPlat
                                text: "Ratio max platine:"
                                Layout.preferredWidth: 130
                                color : Theme.grey_6
                            }
                            CTextField{
                                id: ratioPlat
                                text: "1"
                                Layout.preferredWidth: 150
                                validator: RegExpValidator{regExp: /^[0-1]{0,1}[.][0-9]{0,1}([0-9]{0,1})?([0-9]{0,1})?/}
                                opacity: enabled?1:0.6
                                objectName: "RatioMaxPlat"

                            }
                        }
                        RowLayout{
                            spacing: 15
                            anchors.right: parent.right
                            anchors.left: parent.left
                            anchors.leftMargin: 15
                            anchors.rightMargin: 20
                            Label{
                                id: labelRatioEtr
                                text: "Ratio max étriers:"
                                Layout.preferredWidth: 130
                                color : Theme.grey_6
                            }
                            CTextField{
                                id: ratioetr
                                text: "1"
                                Layout.preferredWidth: 150
                                validator: RegExpValidator{regExp: /^[0-1]{0,1}[.][0-9]{0,1}([0-9]{0,1})?([0-9]{0,1})?/}
                                opacity: enabled?1:0.6
                                objectName: "RatioMaxPlat"

                            }
                        }
                        RowLayout{
                            spacing: 15
                            anchors.right: parent.right
                            anchors.left: parent.left
                            anchors.leftMargin: 15
                            anchors.rightMargin: 20
                            Label{
                                id: labelRatioChev
                                text: "Ratio max chevilles:"
                                Layout.preferredWidth: 130
                                color : Theme.grey_6
                            }
                            CTextField{
                                id: ratioChev
                                text: "1"
                                Layout.preferredWidth: 150
                                validator: RegExpValidator{regExp: /^[0-1]{0,1}[.][0-9]{0,1}([0-9]{0,1})?([0-9]{0,1})?/}
                                opacity: enabled?1:0.6
                                objectName: "RatioMaxChev"

                            }
                        }
                        RowLayout{
                            spacing: 15
                            anchors.right: parent.right
                            anchors.left: parent.left
                            anchors.leftMargin: 15
                            anchors.rightMargin: 20
                            Label{
                                text: "Portée (mm):"
                                Layout.preferredWidth: 130
                                color : Theme.grey_6
                            }
                            CTextField{
                                id: porteprof
                                text: "0"
                                Layout.preferredWidth: 150
                                validator: IntValidator
                                opacity: enabled?1:0.6
                                objectName: "Portee"
                                onEditingFinished: pageGeo.porte = porteprof.text
                            }
                        }

                    }                    
                }
            }
        }
    }
}


