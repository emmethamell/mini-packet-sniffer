import QtQuick
import QtQuick.Controls 
import "components"

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Packet Analyzer"

    header: Header {
        width: parent.width
        height: 20
    }

    // The datasource
    ListModel {
        id: packetModel
        ListElement { srcIP: "192.168.1.1"; dstIP: "8.8.8.8"; protocol: "TCP"; size: "64B" }
        ListElement { srcIP: "192.168.1.2"; dstIP: "8.8.4.4"; protocol: "UDP"; size: "128B" }
        ListElement { srcIP: "192.168.1.2"; dstIP: "8.8.4.4"; protocol: "UDP"; size: "128B" }
        ListElement { srcIP: "192.168.1.2"; dstIP: "8.8.4.4"; protocol: "UDP"; size: "128B" }
        ListElement { srcIP: "192.168.1.1"; dstIP: "8.8.8.8"; protocol: "TCP"; size: "64B" }
    }


    // Custom PacketListView component
    PacketListView {
        width: parent.width
        height: parent.height - 20
        model: packetModel  // Bind the ListModel to the ListView in PacketListView
    }

}