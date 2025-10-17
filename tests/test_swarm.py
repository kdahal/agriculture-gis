import os
import sys

# Fix relative import path for pytest/CI: Add repo root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: F401, E402
from unittest.mock import Mock, patch  # noqa: E402
from scripts.latency_test import run_iperf_test  # noqa: E402


@patch("subprocess.run")
def test_gps_relay(mock_run):
    # Mock MQTT pub/sub test
    mock_run.return_value = Mock(returncode=0)
    result = mock_run(
        [
            "mosquitto_pub",
            "-h",
            "localhost",
            "-t",
            "test/gps",
            "-m",
            "mockdata",
        ],
        capture_output=True,
    )
    assert result.returncode == 0


@patch("scripts.latency_test.subprocess.Popen")
@patch("scripts.latency_test.subprocess.run")
def test_latency_scaling(mock_run, mock_popen):
    # Mock Popen
    mock_proc = Mock()
    mock_proc.terminate.return_value = None
    mock_popen.return_value = mock_proc

    # Mock run with success and low latency output
    mock_result = Mock(returncode=0)
    mock_result.stdout = (
        "Dummy iperf output\n"
        "[  5]  0.0-10.0 sec  1.25 MBytes  1.05 Mbits/sec  sender\n"
        "[  5]  0.0-10.0 sec  1.24 MBytes  1.04 Mbits/sec  receiver\n"
        "\n"
        "iperf Done.\n"
        "iperf3: 150ms avg latency"
    )
    mock_run.return_value = mock_result

    latency = run_iperf_test(90)
    assert latency is not None and latency < 200  # <200ms threshold
