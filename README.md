# ping_scanner
# 🌐 Cloudflare Domain Scanner

A high-performance asynchronous Python tool for scanning domains, detecting Cloudflare IP ranges via CIDR matching, and testing ICMP reachability with real-time progress tracking.

---

## ⚠️ Disclaimer

This tool is intended for:

- Educational purposes  
- Network research  
- Authorized security testing  

🚫 Do not use this tool against systems you do not own or have explicit permission to test.

---

## 🚀 Features

- ⚡ Fully asynchronous scanning (high performance)
- 🌍 CIDR-based IP range detection
- 📡 DNS resolution (Windows-safe)
- 📶 ICMP ping testing
- 📊 Real-time progress bar (`tqdm`)
- ⚙️ Fully configurable via external files
- 💾 Streaming output (safe for millions of domains)
- 🔁 Simple and extendable architecture

---



## ⚙️ Configuration

### settings.txt

CONCURRENCY=500
PING_TIMEOUT=1000


| Parameter     | Description                          |
|--------------|--------------------------------------|
| CONCURRENCY  | Number of async workers              |
| PING_TIMEOUT | ICMP ping timeout in milliseconds    |

---

## 🌐 Cloudflare Ranges

The `ranges.txt` file contains IPv4 CIDR blocks used to detect Cloudflare infrastructure.

These ranges belong to:

Cloudflare, Inc. (global CDN provider)

Example:
173.245.48.0/20
103.21.244.0/22
104.16.0.0/13
172.64.0.0/13


---

## 📥 domains.txt
example.com
google.com
chatgpt.com
github.com

📜 License

MIT License
