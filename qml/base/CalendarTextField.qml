import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Controls 2.0

CustomTextField{
    id:datedebutTF
    placeholderText: "JJ/MM/AAAA"
    validator: RegExpValidator{regExp: /^(0[1-9]|[1-2][0-9]|3[0-1])[/](0[1-9]|1[0-2])[/][0-9]{4}$/}
    onAccepted: datedebutCal.close()
    MouseArea{
        id:ma
        anchors.fill:parent
        onClicked:{
            datedebutTF.forceActiveFocus()
            datedebutCal.open()
        }
    }
    Popup{
        id:datedebutCal
        visible:false
        width:400*wRatio
        height : 0.9*width
        padding: 0
        y: ma.y+ma.height
        x:ma.x+(ma.width-datedebutCal.width)/2
        CustomCalendar{
            anchors.fill: parent
            onClicked:{
                if(selectedDate.getDay()!==6 && selectedDate.getDay()!==0){
                datedebutTF.text = Qt.formatDate(selectedDate,"dd/MM/yyyy")
                datedebutTF.editingFinished()
                datedebutCal.close()}
            }
        }
    }
}
