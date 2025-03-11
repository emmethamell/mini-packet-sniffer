import QtQuick 
import QtQuick.Controls 

ListView {
    width: parent.width
    height: parent.height

    model: ListModel {}

    // Delegate for displaying each packet
    delegate: PacketItem {
        srcIP: model.srcIP
        dstIP: model.dstIP
        protocol: model.protocol
        size: model.size
    }
}