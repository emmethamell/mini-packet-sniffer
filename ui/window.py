from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QTableWidget, QTableWidgetItem, QHeaderView, 
                           QPushButton, QHBoxLayout, QComboBox, QLabel,
                           QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
import sys
import psutil
from packet_sniffer.main import PacketSnifferManager

class PacketAnalyzerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.packet_manager = PacketSnifferManager(callback=self.new_packet_received)
        self.init_ui()
        
        # Setup auto-update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(1000)  # Update every second
        
    def init_ui(self):
        # Main window setup
        self.setWindowTitle("Packet Analyzer")
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Control panel (top section)
        control_panel = QHBoxLayout()
        
        # Interface selection
        self.interface_combo = QComboBox()
        self.populate_interfaces()
        control_panel.addWidget(QLabel("Interface:"))
        control_panel.addWidget(self.interface_combo)
        
        # Filter field
        control_panel.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.setEditable(True)
        self.filter_combo.addItems(["", "tcp", "udp", "icmp", "tcp port 80", "port 443"])
        control_panel.addWidget(self.filter_combo)
        
        # Start/Stop buttons
        self.start_button = QPushButton("Start Capture")
        self.start_button.clicked.connect(self.start_capture)
        control_panel.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Capture")
        self.stop_button.clicked.connect(self.stop_capture)
        self.stop_button.setEnabled(False)
        control_panel.addWidget(self.stop_button)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_data)
        control_panel.addWidget(self.clear_button)
        
        layout.addLayout(control_panel)
        
        # Create and setup table
        self.packet_table = QTableWidget()
        self.packet_table.setColumnCount(4)
        self.packet_table.setHorizontalHeaderLabels(["Source", "Destination", "Protocol", "Size"])
        
        # Style the header
        self.packet_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #333;
                color: white;
                font-weight: bold;
                padding: 4px;
                height: 20px;
            }
        """)
        
        # Make columns stretch
        header = self.packet_table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        # Style the table
        self.packet_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 10px;
                background-color: #f4f4f4;
            }
        """)
        
        layout.addWidget(self.packet_table)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Setup initial table with empty data
        self.packet_table.setRowCount(0)
    
    def populate_interfaces(self):
        """Populate the interface combo box with available network interfaces"""
        self.interface_combo.clear()
        
        try:
            interfaces = list(psutil.net_if_stats().keys())
            self.interface_combo.addItem("Any")
            for interface in interfaces:
                self.interface_combo.addItem(interface)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load network interfaces: {e}")
    
    def start_capture(self):
        """Start capturing packets"""
        interface = self.interface_combo.currentText()
        if interface == "Any":
            interface = None  # Scapy uses None for "any interface"
            
        filter_text = self.filter_combo.currentText()
        
        try:
            if self.packet_manager.start_capture(interface, filter_text):
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.interface_combo.setEnabled(False)
                self.filter_combo.setEnabled(False)
                self.status_bar.showMessage("Capturing packets...")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start packet capture: {e}")
    
    def stop_capture(self):
        """Stop capturing packets"""
        try:
            if self.packet_manager.stop_capture():
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.interface_combo.setEnabled(True)
                self.filter_combo.setEnabled(True)
                self.status_bar.showMessage("Capture stopped")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stop packet capture: {e}")
    
    def clear_data(self):
        """Clear the packet table and analyzer data"""
        self.packet_table.setRowCount(0)
        self.packet_manager.clear_data()
        self.status_bar.showMessage("Data cleared")
    
    def new_packet_received(self, packet_info):
        """Callback function that's called when a new packet is received"""
        # This will be called from a different thread, so we don't update UI directly
        # The UI will be updated periodically by update_ui method
        pass
    
    def update_ui(self):
        """Update the UI with the latest packet data"""
        packets = self.packet_manager.get_packets()
        stats = self.packet_manager.get_stats()
        
        # Update status bar with stats
        self.status_bar.showMessage(
            f"Total Packets: {stats['total_packets']} | "
            f"Protocols: {len(stats['protocols'])} | "
            f"Sources: {len(stats['sources'])} | "
            f"Destinations: {len(stats['destinations'])}"
        )
        
        # Update table with new packets
        current_rows = self.packet_table.rowCount()
        if len(packets) > current_rows:
            # Only add new rows
            self.packet_table.setRowCount(len(packets))
            
            for row in range(current_rows, len(packets)):
                packet = packets[row]
                for col, key in enumerate(['source', 'destination', 'protocol', 'size']):
                    item = QTableWidgetItem(str(packet[key]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.packet_table.setItem(row, col, item)
            
            # Scroll to bottom to show newest packets
            self.packet_table.scrollToBottom()

def main():
    app = QApplication(sys.argv)
    window = PacketAnalyzerWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()