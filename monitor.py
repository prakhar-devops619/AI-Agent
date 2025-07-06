from prometheus_api_client import PrometheusConnect
import time

PROM_URL = "http://localhost:9090"
THRESHOLD = 80.0
DURATION = 120  # seconds
INTERVAL = 15

prom = PrometheusConnect(url=PROM_URL, disable_ssl=True)

def is_cpu_spike():
    result = prom.custom_query("100 - (avg by(instance)(irate(node_cpu_seconds_total{mode='idle'}[1m])) * 100)")
    if result:
        usage = float(result[0]['value'][1])
        print(f"CPU Usage: {usage:.2f}%")
        return usage > THRESHOLD
    return False

def is_memory_spike():
    result = prom.custom_query("100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))")
    if result:
        usage = float(result[0]['value'][1])
        print(f"Memory Usage: {usage:.2f}%")
        return usage > THRESHOLD
    return False

def is_disk_spike():
    result = prom.custom_query("100 * (node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes")
    if result:
        usage = float(result[0]['value'][1])
        print(f"Disk Usage: {usage:.2f}%")
        return usage > THRESHOLD
    return False

def is_any_spike():
    return is_cpu_spike() or is_memory_spike() or is_disk_spike()

def wait_for_duration():
    start = time.time()
    while time.time() - start < DURATION:
        if not is_any_spike():
            return False
        time.sleep(INTERVAL)
    return True
