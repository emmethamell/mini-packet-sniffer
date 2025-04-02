from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether
import threading
import time


class PacketSniffer:
    def __init__(self, callback=None):
        self.callback = callback
        self.running = False
        self.sniff_thread = None
        self.packet_count = 0

    def start_sniffing(self, interface=None, filter=""):
        """Start sniffing packets on the specified interface"""
        if self.running:
            return
        
        self.running = True
        self.packet_count = 0
        
        # Start sniffing in a separate thread
        self.sniff_thread = threading.Thread(
            target=self._sniff_packets,
            args=(interface, filter),
            daemon=True
        )
        self.sniff_thread.start()
        
        return True
    
    def stop_sniffing(self):
        """Stop the packet sniffer"""
        self.running = False
        if self.sniff_thread:
            self.sniff_thread.join(timeout=1.0)
            self.sniff_thread = None
        return True
    
    def _sniff_packets(self, interface, filter):
        """Internal method that runs in a thread to sniff packets"""
        try:
            sniff(
                iface=interface,
                filter=filter,
                prn=self._process_packet,
                store=False,
                stop_filter=lambda _: not self.running
            )
        except Exception as e:
            print(f"Sniffing error: {e}")
            self.running = False
    
    def _process_packet(self, packet):
        """Process a captured packet and call the callback if set"""
        self.packet_count += 1
        
        # Extract packet information
        packet_info = self._extract_packet_info(packet)
        
        # Call the callback function if provided
        if self.callback and packet_info:
            self.callback(packet_info)
        
        return packet_info
    
    def _extract_packet_info(self, packet):
        """Extract relevant information from a packet"""
        info = {
            'source': '',
            'destination': '',
            'protocol': '',
            'size': f"{len(packet)}B"
        }
        
        # Get IP information if available
        if IP in packet:
            info['source'] = packet[IP].src
            info['destination'] = packet[IP].dst
            
            # Determine protocol
            if TCP in packet:
                info['protocol'] = f"TCP {packet[TCP].sport} → {packet[TCP].dport}"
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    info['protocol'] = "HTTP"
                elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
                    info['protocol'] = "HTTPS"
            elif UDP in packet:
                info['protocol'] = f"UDP {packet[UDP].sport} → {packet[UDP].dport}"
                if packet[UDP].dport == 53 or packet[UDP].sport == 53:
                    info['protocol'] = "DNS"
            else:
                info['protocol'] = packet[IP].proto
        elif Ether in packet:
            info['source'] = packet[Ether].src
            info['destination'] = packet[Ether].dst
            info['protocol'] = packet[Ether].type
        
        return info
