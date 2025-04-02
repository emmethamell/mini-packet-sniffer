from collections import defaultdict, Counter

class PacketAnalyzer:
    def __init__(self):
        self.packets = []
        self.stats = {
            'total_packets': 0,
            'protocols': Counter(),
            'sources': Counter(),
            'destinations': Counter(),
            'packet_sizes': []
        }
    
    def add_packet(self, packet_info):
        """Add a packet to the analyzer and update statistics"""
        self.packets.append(packet_info)
        self.stats['total_packets'] += 1
        self.stats['protocols'][packet_info['protocol']] += 1
        self.stats['sources'][packet_info['source']] += 1
        self.stats['destinations'][packet_info['destination']] += 1
        
        # Extract numeric size
        try:
            size = int(packet_info['size'].rstrip('B'))
            self.stats['packet_sizes'].append(size)
        except ValueError:
            pass
    
    def get_packets(self, limit=None):
        """Get the list of packets, optionally limiting the number returned"""
        if limit:
            return self.packets[-limit:]
        return self.packets
    
    def get_stats(self):
        """Get the current statistics"""
        stats = self.stats.copy()
        
        # Calculate average packet size
        if self.stats['packet_sizes']:
            stats['avg_packet_size'] = sum(self.stats['packet_sizes']) / len(self.stats['packet_sizes'])
        else:
            stats['avg_packet_size'] = 0
            
        # Get most common protocol, source, and destination
        stats['most_common_protocol'] = self.stats['protocols'].most_common(1)[0] if self.stats['protocols'] else None
        stats['most_common_source'] = self.stats['sources'].most_common(1)[0] if self.stats['sources'] else None
        stats['most_common_destination'] = self.stats['destinations'].most_common(1)[0] if self.stats['destinations'] else None
        
        return stats
    
    def clear(self):
        """Clear all collected data"""
        self.packets = []
        self.stats = {
            'total_packets': 0,
            'protocols': Counter(),
            'sources': Counter(),
            'destinations': Counter(),
            'packet_sizes': []
        }
