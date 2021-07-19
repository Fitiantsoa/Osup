import QtQuick 2.9
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0

import "theme.js" as Theme
import "./base"
import "./ui"
import "./components"
import "./views"
import "../assets/fonts/"

ApplicationWindow {
    id: applicationWindow
    height: 600
    width: 800
    visible: true
    title: qsTr(osup.get_version())
    onClosing: {
        osup.write_recent_file()
        if (osup.get_saved_state()){
            osup.close_console()
            close.accepted=true
        }
        else{
            close.accepted=false
            saveOnClose.open()
        }
    }
    FontLoader { id: localFont; source: "../assets/fonts/fontello.ttf" }
    FontLoader { id: greek; source: "../assets/fonts/greekc__.ttf" }
    property var component;
    property variant adminWindow;
    property variant dbWindow
    Component.onCompleted: applicationWindow.showMaximized()
    menuBar: CMenuBar {
        id: menuBar
        height: 27
        background: Rectangle { color: Theme.background }
        CMenu{
            title: "Fichier"
            Action{text: qsTr("Ouvrir"); shortcut: StandardKey.Open; onTriggered:openDialog.open()}
            Action{text: qsTr("Importer courbe"); shortcut: StandardKey.Open; onTriggered:openDialogImport.open()}
            Action{text: qsTr("Sauvegarder"); shortcut: StandardKey.Save; onTriggered:osup.save_to_file()}
            Action{text: qsTr("Sauvegarder sous ..."); shortcut: StandardKey.SaveAs; onTriggered:saveDialog.open()}
            MenuSeparator { }
            Action{text: qsTr("Quitter"); shortcut: StandardKey.Quit; onTriggered: applicationWindow.close()}
        }
        CMenu{
            title: "Outils"
            Action{text: qsTr("Afficher les logs"); onTriggered:osup.open_console()}
            Action{text: qsTr("Historique des versions"); onTriggered:{releaseWindows.show();osup.getTextRelease()}}
        }
    }
    ToolBar {
        id : tb
        height: 28
        width : parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        background: Rectangle { color: Theme.background }
        MessageDialog{
            id : errorMessageDialog
            objectName: "ErrorMessageDialog"
            title: "Une erreur est survenue !"
            buttons: StandardButton.Ok
            onOkClicked: errorMessageDialog.close()
        }
        MessageDialog{
            id: saveOnClose
            objectName: "workNotSavedOnClose"
            title: applicationWindow.title
            text: "Votre travail n'a pas été sauvegardé. Voulez-vous l'enregistrer ?"
            buttons: StandardButton.No | StandardButton.Save | StandardButton.Cancel
            onNoClicked: {
                close.accepted=true
                Qt.quit()
            }
            onSaveClicked: osup.save_before_close()
        }
        Column {
            width: parent.width
            height: parent.height
            spacing: 1
            Rectangle {
                height: 1
                width: parent.width
                anchors.horizontalCenter: parent.horizontalCenter
                color: Theme.grey_2
            }
            Row {
                id: fileRow2
                spacing: 10
                height: 25
                width: parent.width
                anchors.leftMargin: 20
                anchors.left: parent.left
                ButtonTool {
                    id: newButton
                    text: "\uE814"
                    font.family: "fontello"
                    onClicked: osup.new_file()
                    toolTipText:  "Nouveau Fichier"
                    toolTipx: newButton.x- 150/2
                    Shortcut{
                        sequence: StandardKey.New
                        onActivated: osup.new_file()
                    }
                    MessageDialog{
                        id: messageDialog
                        objectName: "workNotSaved"
                        title: applicationWindow.title
                        text: "Votre travail n'a pas été sauvegardé. Voulez-vous l'enregistrer ?"
                        buttons: StandardButton.No | StandardButton.Save | StandardButton.Cancel
                        onNoClicked: osup.force_new_file()
                        onSaveClicked: osup.save_before_new_file()
                    }
                }
                ButtonTool {
                    id: openButton
                    text: "\uF115"
                    font.family: "fontello"
                    onClicked: openDialog.open()
                    toolTipText: "Ouvrir Fichier"
                    toolTipx: openButton.x - newButton.width - 150/2
                    Shortcut{
                        sequence: StandardKey.Open
                        onActivated: openDialog.open()
                    }
                    FileDialog {
                        id: openDialog
                        objectName: "openDialog"
                        fileMode: FileDialog.OpenFile
                        selectedNameFilter.index: 0
                        nameFilters: ["OSup files (*.osup)"]
                        folder: "../"
                        onAccepted: osup.read_from_file(file,folder)
                    }
                }
                ButtonTool {
                    id: importButton
                    text: "\uF115"
                    font.family: "fontello"
                    onClicked: openDialogImport.open()
                    toolTipText: "Importer courbe"
                    toolTipx: openButton.x - newButton.width - 150/2
                    Shortcut{
                        sequence: StandardKey.Open
                        onActivated: openDialogImport.open()
                    }
                    FileDialog {
                        id: openDialogImport
                        objectName: "openDialogImport"
                        fileMode: FileDialog.OpenFile
                        selectedNameFilter.index: 0
                        nameFilters: ["OSup files (*.rosup)"]
                        folder: "../"
                        onAccepted: osup.import_curve(file,folder)
                    }
                }
                ButtonTool {
                    id: savebutton
                    text: "\uE80F"
                    font.family: "fontello"
                    onClicked: osup.save_to_file()
                    toolTipText: "Enregistrer"
                    toolTipx: savebutton.x - 2*newButton.width-150/2
                    Shortcut{
                        sequence: StandardKey.Save
                        onActivated: osup.save_to_file()
                    }
                }
                ButtonTool {
                    id: saveAs
                    text: "\uE80E"
                    font.family: "fontello"
                    onClicked: saveDialog.open()
                    toolTipText: "Enregistre sous..."
                    toolTipx: saveAs.x - 3*newButton.width-150/2
                    Shortcut{
                        sequence: "Ctrl+Shift+S"
                        onActivated: saveDialog.open()
                    }
                    FileDialog {
                        id: saveDialog
                        objectName: "saveAsDialog"
                        fileMode: FileDialog.SaveFile
                        nameFilters: openDialog.nameFilters
                        selectedNameFilter.index: 0
                        folder: "../"
                        onAccepted: osup.save_to_file_as(file)
                    }
                }
                ToolSeparator {
                    height: 21
                    anchors.verticalCenter: parent.verticalCenter
                }
                ButtonConsoleLog {
                    id: displayConsole
                    objectName: "displayConsole"
                    text: "\uE851"
                    font.family: "fontello"
                    onClicked: {
                        displayConsole.errorEdited = false
                        osup.open_console()
                    }
                    toolTipText: "Ouvrir log Console"
                    toolTipx: displayConsole.x - 4*newButton.width - 150/2
                }
                ToolSeparator {
                    height: 21
                    anchors.verticalCenter: parent.verticalCenter
                }
                ButtonTool {
                    id: aPropo
                    text: "\uF086"
                    font.family: "fontello"
                    toolTipText: "A propos"
                    onClicked:aProposDialog.open()
                }
                MessageDialog{
                    id: aProposDialog
                    title: "A propos"
                    text: " <p style='text-align:center;'></p>
                            <br>
                            <br> Developpé par:
                            <br>
                            <br>
                            <br>2021 - Propriété de SOM CALCUL"
                    buttons: StandardButton.Close
                    onCloseClicked:aProposDialog.close()
                }
                ButtonTool {
                    id: help
                    text: "\uE80C"
                    font.family: "fontello"
                    toolTipText: "Aide"
//                    onClicked:{
//                        osup.openManual()
//                    }
                }
                Rectangle {
                    color: "transparent"
                    height: parent.height
                    width: parent.width - 370
                    anchors.verticalCenter: parent.verticalCenter
                }
                ToolSeparator {
                    height: 21
                    anchors.verticalCenter: parent.verticalCenter
                }
                ButtonTool{
                    id : dbButton
                    text: "\uE854"
                    font.family: "fontello"
                    toolTipText: "Gestion des bases de données"
                    objectName: "DbButton"
                    opacity: enabled ? 1 : 0.5
                    onClicked: {
                        var component2 = Qt.createComponent("./views/DbMenu.qml");
                        dbWindow = component2.createObject(applicationWindow);
                        //                 dbWindow.closing.connect(dbWindow.closing)
                        osup.init_data_manager(dbWindow)
                        dbWindow.show();
                    }
                }
//                ButtonTool {
//                    id: adminButton
//                    text: "\uF2BE"
//                    font.family: "fontello"
//                    toolTipText: "Menu Administrateur"
//                    objectName: "AdminButton"
//                    opacity: enabled ? 1 : 0.5
//                    onClicked:{
//                        if (applicationWindow.adminOpen === false){
//                            var component = Qt.createComponent("./views/AdminMenu.qml");
//                            adminWindow = component.createObject(applicationWindow)
//                            otau.scanPC(listePC)
//                            otau.scanUser(listeUser)
//                            adminWindow.show()
//                            applicationWindow.adminOpen=true}
//                        else {
//                            adminWindow.show()
//                        }
//                    }
//                }
            }
            Rectangle {
                height: 1
                width: parent.width
                anchors.horizontalCenter: parent.horizontalCenter
                color: Theme.grey_2
            }
        }
    }
    Rectangle {
        id: loaders
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.top: tb.bottom
        anchors.topMargin: 1
        StackLayout {
            id: loader
            anchors.fill: parent
            focus: true
            currentIndex: 0
            Page0{ id: page0 }
            PageMain{ id : pageMain }
        }
    }
}
