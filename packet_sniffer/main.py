from packet_sniffer.sniffer import PacketSniffer
from packet_sniffer.analyzer import PacketAnalyzer

class PacketSnifferManager:
    def __init__(self, callback=None):
        self.sniffer = PacketSniffer(callback=self._packet_callback)
        self.analyzer = PacketAnalyzer()
        self.user_callback = callback
    
    def start_capture(self, interface=None, filter=""):
        """Start capturing packets"""
        return self.sniffer.start_sniffing(interface, filter)
    
    def stop_capture(self):
        """Stop capturing packets"""
        return self.sniffer.stop_sniffing()
    
    def get_packets(self, limit=None):
        """Get captured packets"""
        return self.analyzer.get_packets(limit)
    
    def get_stats(self):
        """Get packet statistics"""
        return self.analyzer.get_stats()
    
    def clear_data(self):
        """Clear all captured data"""
        self.analyzer.clear()
    
    def _packet_callback(self, packet_info):
        """Internal callback that updates the analyzer and calls the user callback"""
        self.analyzer.add_packet(packet_info)
        
        if self.user_callback:
            self.user_callback(packet_info)
