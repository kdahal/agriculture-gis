#!/usr/bin/env python3
import subprocess
import logging
import argparse
import os
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('/var/log/latency-test.log'), logging.StreamHandler()])

def run_iperf_test(nodes, duration=10):
    logger = logging.getLogger(__name__)
    base_cmd = ['iperf3', '-s']  # Server on ground
    client_cmd = ['iperf3', '-c', '192.168.1.1', '-t', str(duration), '-P', str(nodes // 10)]  # Parallel clients

    try:
        # Start server in bg
        proc = subprocess.Popen(base_cmd)
        sleep(2)
        result = subprocess.run(client_cmd, capture_output=True, text=True, timeout= duration + 5)
        proc.terminate()
        if result.returncode == 0:
            logger.info(f"Latency test passed: {result.stdout}")
            return float(result.stdout.split()[-1]) if 'ms' in result.stdout else 0  # Parse avg latency
        else:
            logger.error(f"Test failed: {result.stderr}")
            return None
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--nodes', type=int, default=os.getenv('TEST_NODES', 90))
    args = parser.parse_args()
    latency = run_iperf_test(args.nodes)
    if latency:
        print(f"Avg Latency: {latency}ms")
    else:
        exit(1)