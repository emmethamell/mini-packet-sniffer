import QtQuick
import QtQuick.Controls 
import QtQuick.Layouts

Item {
    width: parent.width
    height: 20

    Rectangle {
        width: parent.width
        height: 20
        color: "#333"

        GridLayout {
            columns: 4 

            Text {
                text: "Source"
                color: "white"
                font.bold: true
            }

            Text {
                text: "Destination"
                color: "white"
                font.bold: true  
            }

            Text {
                text: "Protocol"
                color: "white"
                font.bold: true      
            }
            
            Text {
                text: "Size"
                color: "white"
                font.bold: true
            }
        }
    }
}