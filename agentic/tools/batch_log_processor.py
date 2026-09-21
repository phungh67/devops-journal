import re
from collections import defaultdict
from typing import List, Dict, Any

class BatchLogProcessor:
    def __init__(self, log_pattern: str = r"\[(.*?)\] (.*)"):
        """
        Initializes the processor.
        
        Args:
            log_pattern: A regex string where group 1 is the timestamp 
                         and group 2 is the core log message.
                         Default matches format: [2026-09-21 09:14:02] Connection Timeout...
        """
        self.log_pattern = re.compile(log_pattern)

    def process_logs(self, log_lines: List[str]) -> List[Dict[str, Any]]:
        """
        Aggregates logs by message content, favoring sequential timestamps.
        
        Returns a list of dictionaries containing the message, count, and timestamps.
        """
        aggregated_logs = defaultdict(lambda: {"count": 0, "timestamps": []})
        
        for line in log_lines:
            line = line.strip()
            if not line:
                continue
                
            match = self.log_pattern.search(line)
            if match:
                timestamp = match.group(1).strip()
                raw_message = match.group(2).strip()
                normalized_message = self._normalize_message(raw_message)
                
                aggregated_logs[normalized_message]["count"] += 1
                aggregated_logs[normalized_message]["timestamps"].append(timestamp)
            else:
                aggregated_logs[line]["count"] += 1
                aggregated_logs[line]["timestamps"].append("UNKNOWN_TIME")

        # Convert the defaultdict to the final structured list for the LLM context
        final_output = []
        for message, data in aggregated_logs.items():
            final_output.append({
                "message": message,
                "count": data["count"],
                "first_seen": data["timestamps"][0] if data["timestamps"] else None,
                "last_seen": data["timestamps"][-1] if data["timestamps"] else None
            })
            
        return sorted(final_output, key=lambda x: x["count"], reverse=True)

    def _normalize_message(self, message: str) -> str:
        """Removes volatile data like UUIDs or specific IPs for better grouping."""
        message = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>', message, flags=re.IGNORECASE)
        message = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', message)
        message = re.sub(r'\b\d+\b', '<NUM>', message)
        return message


# --- Example Usage based on the architecture diagram ---
if __name__ == "__main__":
    sample_logs = [
        "[2026-09-21 09:14:02] payments-api: latency p99 climbed to 4s",
        "[2026-09-21 09:14:05] ERROR 503 from backend service at 192.168.1.5",
        "[2026-09-21 09:14:06] ERROR 503 from backend service at 192.168.1.6",
        "[2026-09-21 09:14:08] ERROR 503 from backend service at 192.168.1.5",
        "[2026-09-21 09:14:15] payments-api: latency p99 climbed to 4s"
    ]

    processor = BatchLogProcessor()
    aggregated_dict = processor.process_logs(sample_logs)
    
    import json
    print(json.dumps(aggregated_dict, indent=2))