import asyncio
import socket
import ipaddress
from tqdm import tqdm
from datetime import datetime

# ==============================
# FILES
# ==============================
INPUT_FILE = "domains.txt"
RANGES_FILE = "ranges.txt"
SETTINGS_FILE = "settings.txt"
OUTPUT_FILE = "results.txt"

# ==============================
# LOAD SETTINGS
# ==============================
def load_settings(filename):
    settings = {
        "CONCURRENCY": 500,
        "PING_TIMEOUT": 1000,
    }

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if key in settings:
                    try:
                        settings[key] = int(value)
                    except ValueError:
                        print(f"[!] Invalid value for {key}: {value}")
    except FileNotFoundError:
        print(f"[!] settings file not found: {filename}")
        print("[!] Using default settings")

    print(f"[+] Settings loaded: {settings}")
    return settings


SETTINGS = load_settings(SETTINGS_FILE)
CONCURRENCY = SETTINGS["CONCURRENCY"]
PING_TIMEOUT = SETTINGS["PING_TIMEOUT"]

# ==============================
# LOAD CLOUDFLARE RANGES
# ==============================
def load_cf_ranges(filename):
    networks = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                try:
                    networks.append(ipaddress.ip_network(line))
                except ValueError:
                    print(f"[!] Invalid CIDR skipped: {line}")

    except FileNotFoundError:
        print(f"[!] ranges file not found: {filename}")
        exit(1)

    print(f"[+] Loaded {len(networks)} Cloudflare ranges")
    return networks


CF_NETWORKS = load_cf_ranges(RANGES_FILE)

# ==============================
# HELPERS
# ==============================
def is_cloudflare_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return any(ip_obj in net for net in CF_NETWORKS)
    except:
        return False


async def resolve_domain(domain):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, socket.gethostbyname, domain)
    except:
        return None


async def ping_ip(ip):
    try:
        proc = await asyncio.create_subprocess_exec(
            "ping", "-n", "1", "-w", str(PING_TIMEOUT), ip,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL
        )
        stdout, _ = await proc.communicate()

        return b"TTL=" in stdout
    except:
        return False


# ==============================
# WORKER
# ==============================
async def process_domain(domain, sem, stats, file_lock, outfile):
    async with sem:
        stats["scanned"] += 1

        ip = await resolve_domain(domain)
        if not ip:
            stats["dns_fail"] += 1
            return

        stats["resolved"] += 1

        if not is_cloudflare_ip(ip):
            return

        stats["cloudflare"] += 1

        ping_ok = await ping_ip(ip)
        if ping_ok:
            stats["ping_ok"] += 1

        async with file_lock:
            outfile.write(f"{domain},{ip},{ping_ok}\n")


# ==============================
# MAIN
# ==============================
async def main():
    # Load domains
    try:
        with open(INPUT_FILE, "r") as f:
            domains = [d.strip() for d in f if d.strip()]
    except FileNotFoundError:
        print(f"[!] domain file not found: {INPUT_FILE}")
        return

    total = len(domains)

    stats = {
        "scanned": 0,
        "resolved": 0,
        "dns_fail": 0,
        "cloudflare": 0,
        "ping_ok": 0
    }

    sem = asyncio.Semaphore(CONCURRENCY)
    file_lock = asyncio.Lock()

    start_time = datetime.now()

    with open(OUTPUT_FILE, "w", buffering=1) as outfile:
        pbar = tqdm(total=total, desc="Scanning", unit="domain")

        async def worker(domain):
            await process_domain(domain, sem, stats, file_lock, outfile)
            pbar.update(1)

        tasks = [worker(d) for d in domains]

        for coro in asyncio.as_completed(tasks):
            await coro

        pbar.close()

    elapsed = datetime.now() - start_time

    # ==============================
    # FINAL STATS
    # ==============================
    print("\n=== FINAL STATS ===")
    print(f"Total scanned     : {stats['scanned']}")
    print(f"DNS resolved      : {stats['resolved']}")
    print(f"DNS failed        : {stats['dns_fail']}")
    print(f"Cloudflare domains: {stats['cloudflare']}")
    print(f"Ping success      : {stats['ping_ok']}")
    print(f"Elapsed time      : {elapsed}")


# ==============================
# ENTRY
# ==============================
if __name__ == "__main__":
    asyncio.run(main())