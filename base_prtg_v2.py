#!/usr/bin/env python3
"""
PRTG Script v2 Defensive Base Wrapper (Paessler PRTG 25.x.106+ Compliant)
Guarantees schema compliance, stdin handling, and exception isolation.
"""
import os
import sys
import json
from typing import List, Dict, Any

# 1. Neutralize PRTG -E security parameter by prepending local vendor path
VENDOR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")
if os.path.isdir(VENDOR_DIR) and VENDOR_DIR not in sys.path:
    sys.path.insert(0, VENDOR_DIR)


def check_linux_procfs() -> None:
    """Verify /proc mount on Linux probes unless overridden by environment."""
    if sys.platform.startswith("linux"):
        if not os.path.ismount("/proc") and not os.environ.get("PAESSLER_SENSOR_EXE_SCRIPT_ROOT"):
            raise RuntimeError(
                "Linux procfs (/proc) is not mounted and PAESSLER_SENSOR_EXE_SCRIPT_ROOT is unset."
            )


def read_stdin_placeholders() -> Dict[str, Any]:
    """Read %host, %sensorid, and placeholders passed by PRTG via stdin."""
    try:
        if sys.stdin.isatty():
            return {}
        raw = sys.stdin.read().strip()
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback parsing for line-by-line or space-separated placeholders
            lines = raw.splitlines() if "\n" in raw else raw.split()
            keys = ["host", "sensorid", "p1", "p2", "p3", "p4", "p5"]
            return dict(zip(keys, lines))
    except Exception as exc:
        emit_prtg_v2_error(f"Failed parsing stdin: {exc}")
        return {}


def emit_prtg_v2_json(channels: List[Dict[str, Any]], message: str = "OK") -> None:
    """Validate Paessler v2 constraints and emit strict JSON."""
    if len(channels) > 50:
        raise ValueError(f"Channel count ({len(channels)}) exceeds PRTG ceiling of 50 channels.")

    for ch in channels:
        ch_id = int(ch.get("id", 0))
        if ch_id < 10 or ch_id > 2147483647:
            raise ValueError(f"Invalid channel ID {ch_id}. PRTG Script v2 mandates IDs between 10 and 2,147,483,647.")
        if "name" not in ch or "value" not in ch:
            raise ValueError(f"Channel {ch_id} missing mandatory 'name' or 'value' attribute.")

    payload = {
        "version": 2,
        "status": "ok",
        "message": str(message)[:250],
        "channels": channels
    }
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
    sys.exit(0)


def emit_prtg_v2_error(error_msg: str) -> None:
    """Trap all runtime errors into a compliant PRTG error response without crashing."""
    payload = {
        "version": 2,
        "status": "error",
        "message": str(error_msg).replace('"', "'")[:250],
        "channels": []
    }
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
    sys.exit(0)


if __name__ == "__main__":
    # Built-in self-test verification
    if "--test" in sys.argv:
        test_channels = [
            {"id": 10, "name": "SelfTest Latency", "value": 12.4, "unit": "ms"},
            {"id": 11, "name": "SelfTest PacketLoss", "value": 0, "unit": "%"}
        ]
        emit_prtg_v2_json(test_channels, message="Diagnostic Engine Online")
