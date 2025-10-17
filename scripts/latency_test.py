#!/usr/bin/env python3
import argparse
import logging
import os
import subprocess
from time import sleep


# Portable log path: Create logs/ dir if needed
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "latency-test.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(),
    ],
)


def run_iperf_test(nodes, duration=10):
    logger = logging.getLogger(__name__)
    base_cmd = ["iperf3", "-s"]  # Server on ground
    client_cmd = [
        "iperf3",
        "-c",
        "192.168.1.1",
        "-t",
        str(duration),
        "-P",
        str(nodes // 10),
    ]  # Parallel clients

    try:
        # Start server in bg
        proc = subprocess.Popen(base_cmd)
        sleep(2)
        result = subprocess.run(
            client_cmd,
            capture_output=True,
            text=True,
            timeout=duration + 5,
        )
        proc.terminate()
        if result.returncode == 0:
            logger.info(f"Latency test passed: {result.stdout}")
            # Parse avg latency (simplistic; improve for prod)
            words = result.stdout.split()
            last_word = words[-1] if words else "0"
            return float(last_word.rstrip("ms")) if "ms" in last_word else 0.0
        else:
            logger.error(f"Test failed: {result.stderr}")
            return None
    except Exception as e:
        logger.error(f"Error: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--nodes",
        type=int,
        default=int(os.getenv("TEST_NODES", "90")),
    )
    args = parser.parse_args()
    latency = run_iperf_test(args.nodes)
    if latency:
        print(f"Avg Latency: {latency}ms")
    else:
        exit(1)
