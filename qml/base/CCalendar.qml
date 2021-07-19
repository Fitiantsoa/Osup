import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import "../../Theme.js" as Theme

Calendar {
    id :calendar
    frameVisible:true
    style: CalendarStyle {
        gridVisible: true
        gridColor : "black"
        background: Rectangle{
            height:parent.height
            width:parent.width
            anchors.fill: parent
            color:"black"
        }
        dayDelegate: Rectangle {
            color: (styleData.selected && styleData.date.getDay()!==6 && styleData.date.getDay()!==0) ?  Theme.mainColor3: (styleData.visibleMonth && styleData.valid ? Theme.darkColor1 :Theme.lightColor1);
            Label {
                text: styleData.date.getDate()
                anchors.centerIn: parent
                font.pixelSize: 14*average
                font.bold: true
                color:  styleData.date.getDay()!==6 && styleData.date.getDay()!==0 ?"white" : Theme.LightRed
            }
            opacity: styleData.visibleMonth && styleData.valid /* && styleData.date.getDay()!==6 && styleData.date.getDay()!==0 */? 1 : 0.8
        }
        navigationBar: Rectangle{
            id: rectangle
            color:Theme.mainColor1
            height:calendar.height/6
            width : parent.width
            Rectangle {
                width: parent.width
                height: 1
                color: "black"
                anchors.bottom: parent.bottom
            }
            CalendarButton {
                id: previousYear
                width: 50*wRatio
                height: width
                font.pixelSize: 32*average
                anchors.verticalCenterOffset: -1
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 2
                font.family: "fontello"
                text:"\ue83b"
                onClicked: control.showPreviousYear()
            }
            CalendarButton {
                id: previousMonth
                width: 50*wRatio
                height: width
                font.pixelSize: 32*average
                anchors.verticalCenterOffset: -1
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: previousYear.right
                font.family: "fontello"
                text:"\ue833"
                onClicked: control.showPreviousMonth()
            }
            Label {
                id: dateText
                text: styleData.title
                anchors.verticalCenterOffset: -1
                anchors.verticalCenter: parent.verticalCenter
//                anchors.horizontalCenter: parent.horizontalCenter
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 18*average
                font.bold: true
                anchors.left: previousMonth.right
                anchors.leftMargin: 2
                anchors.right: nextMonth.left
                anchors.rightMargin: 2
                color:"white"
                MouseArea{
                    anchors.fill: dateText
                    hoverEnabled: true
                    id : ma
                }
            }
            CalendarButton {
                id: nextMonth
                width: 50*wRatio
                height: width
                font.pixelSize: 32*average
                font.family: "fontello"
                text:"\ue834"
                anchors.verticalCenterOffset: -1
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: nextYear.left
                onClicked: control.showNextMonth()
            }
            CalendarButton {
                id: nextYear
                width: 50*wRatio
                height: width
                font.pixelSize: 32*average
                font.family: "fontello"
                text:"\ue83d"
                anchors.verticalCenterOffset: -1
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 2
                onClicked: control.showNextYear()
            }
        }
        dayOfWeekDelegate:Rectangle {
            color: Theme.mainColor1
            implicitHeight: 24
            Label {
                text: control.__locale.dayName(styleData.dayOfWeek, control.dayOfWeekFormat)
                anchors.centerIn: parent
                font.pixelSize: 13*average
                font.bold: true
                color:  styleData.dayOfWeek!==6 && styleData.dayOfWeek!==0 ?"white" : Theme.LightRed

            }
        }
    }
}
