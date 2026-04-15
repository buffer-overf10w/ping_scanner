# ping_scanner
🌐 Cloudflare Domain Scanner

A high-performance asynchronous Python tool for scanning domains, detecting Cloudflare IP usage via CIDR ranges, and testing ICMP reachability with real-time progress tracking.

⚠️ Disclaimer

This tool is intended for:

Network research
Educational purposes
Security analysis in authorized environments

🚫 Do NOT use this tool against systems you do not own or have explicit permission to test.

🚀 Features
⚡ Fully asynchronous scanning (high performance)
🌍 CIDR-based IP range detection (Cloudflare networks)
📡 DNS resolution with Windows-safe fallback
📶 ICMP ping testing (Windows ping)
📊 Real-time progress bar (tqdm)
⚙️ Fully configurable via external files
💾 Streaming output (safe for millions of domains)
🔁 Easily extendable architecture
📁 Project Structure
project/
│
├── scanner.py          # Main script
├── domains.txt         # Input domain list
├── ranges.txt          # Cloudflare CIDR ranges
├── settings.txt        # Runtime configuration
└── results.txt         # Output file (generated)
⚙️ Configuration
📌 settings.txt
CONCURRENCY=500
PING_TIMEOUT=1000
Parameter	Description
CONCURRENCY	Number of async workers
PING_TIMEOUT	Ping timeout in milliseconds
📌 ranges.txt

Contains Cloudflare IPv4 CIDR blocks:

173.245.48.0/20
103.21.244.0/22
103.22.200.0/22
104.16.0.0/13
172.64.0.0/13
...

These ranges are used to detect whether a domain resolves to Cloudflare infrastructure.

📌 domains.txt
example.com
google.com
chatgpt.com
github.com

🧱 Technical Stack
Python 3.9+
asyncio
socket
ipaddress
tqdm

📜 License

MIT License — free to use, modify, and distribute.
