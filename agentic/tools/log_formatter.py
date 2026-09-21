import re
import ipaddress

class LogFormatter:
    def __init__(self, retain_public_ips: bool = True):
        """
        Initializes the formatter.
        
        Args:
            retain_public_ips: If True, public IPs are kept in the log to track 
                               external actors. Private IPs are always masked.
        """
        self.retain_public_ips = retain_public_ips
        self.ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

    def format_message(self, message: str) -> str:
        """Evaluates IPs in the message and masks them contextually."""
        
        def ip_evaluator(match):
            ip_str = match.group(0)
            try:
                ip_obj = ipaddress.ip_address(ip_str)
                
                if ip_obj.is_private:
                    # Always mask private VPC/Cluster IPs to group microservice noise
                    return "<PRIVATE_IP>"
                else:
                    # Retain public IPs if configured, otherwise mask them generically
                    if self.retain_public_ips:
                        return f"<PUBLIC_IP: {ip_str}>"
                    return "<PUBLIC_IP>"
                    
            except ValueError:
                # Fallback if regex caught an invalid IP string (e.g., 999.999.999.999)
                return ip_str

        # Apply the IP evaluator replacement
        formatted = self.ip_pattern.sub(ip_evaluator, message)
        
        # Mask other volatile data (UUIDs, trace IDs, etc.)
        formatted = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>', formatted, flags=re.IGNORECASE)
        
        return formatted


# --- Integration with your architecture ---
if __name__ == "__main__":
    formatter = LogFormatter(retain_public_ips=True)
    
    raw_logs = [
        "Connection refused from internal service at 10.0.1.45",
        "Connection refused from internal service at 192.168.1.12",
        "Failed login attempt from external actor at 203.0.113.42",
        "Failed login attempt from external actor at 198.51.100.17"
    ]
    
    for log in raw_logs:
        print(formatter.format_message(log))