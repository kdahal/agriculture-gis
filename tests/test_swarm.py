import pytest
import subprocess
from scripts.latency_test import run_iperf_test  # If modularized

def test_latency_scaling():
    latency = run_iperf_test(90)
    assert latency is not None and latency < 200  # <200ms threshold

def test_gps_relay():
    # Mock MQTT pub/sub test
    result = subprocess.run(['mosquitto_pub', '-h', 'localhost', '-t', 'test/gps', '-m', 'mockdata'], capture_output=True)
    assert result.returncode == 0

# Run: pytest tests/ -v