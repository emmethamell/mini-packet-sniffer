import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Item {
    width: parent.width
    height: 50

    Rectangle {
        width: parent.width
        height: 50
        color: "#f4f4f4"
        border.color: "#ddd"

        GridLayout {
            columns: 4 
            anchors.fill: parent

            Text {
                text: srcIP
            }
            
            Text {
                text: dstIP
            }

            Text {
                text: protocol
            }

            Text {
                text: size
            }
        }
    }

    // Properties that recieve data from the model
    property string srcIP
    property string dstIP
    property string protocol
    property string size
}