#!/usr/bin/env python3
"""
PRTG Script v2 Schema Validator & Pre-Flight Diagnostic Tool
Validates custom sensor JSON output against Paessler PRTG 25.x.106+ specifications.
Open-Source Lead-Magnet Utility.
"""
import sys
import json
import argparse
import subprocess
from typing import Dict, Any, List, Tuple

PAESSLER_MAX_CHANNELS = 50
PAESSLER_MIN_CHANNEL_ID = 10
PAESSLER_MAX_CHANNEL_ID = 2147483647
VALID_STATUSES = {"ok", "error", "warning"}


def validate_v2_payload(raw_json: str) -> Tuple[bool, List[str], Dict[str, Any]]:
    """Strictly audit raw JSON string against Paessler Script v2 constraints."""
    errors = []
    parsed = {}

    # 1. JSON Syntax Validation
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as err:
        return False, [f"JSON Syntax Error (Line {err.lineno}, Col {err.colno}): {err.msg}"], {}

    if not isinstance(parsed, dict):
        return False, ["Root payload must be a JSON Object ({}), not an Array or scalar."], parsed

    # 2. Root Fields Validation
    if parsed.get("version") != 2:
        errors.append(f"Invalid or missing 'version' attribute: Expected integer 2, got {parsed.get('version')!r}.")

    status = str(parsed.get("status", "")).lower()
    if status not in VALID_STATUSES:
        errors.append(f"Invalid 'status': Expected one of {VALID_STATUSES}, got {parsed.get('status')!r}.")

    if "message" in parsed and not isinstance(parsed["message"], str):
        errors.append(f"'message' attribute must be a string, got {type(parsed['message']).__name__}.")

    # 3. Channels Array Validation
    channels = parsed.get("channels")
    if not isinstance(channels, list):
        errors.append(f"'channels' attribute must be a list/array, got {type(channels).__name__}.")
        return False, errors, parsed

    if len(channels) > PAESSLER_MAX_CHANNELS:
        errors.append(
            f"Channel count ({len(channels)}) exceeds PRTG hard operational ceiling of {PAESSLER_MAX_CHANNELS} channels."
        )

    seen_ids = set()
    for idx, ch in enumerate(channels):
        if not isinstance(ch, dict):
            errors.append(f"Channel at index {idx} is not a valid JSON object.")
            continue

        # Check Channel ID
        ch_id = ch.get("id")
        if ch_id is None:
            errors.append(f"Channel at index {idx} ({ch.get('name', 'unnamed')}) is missing mandatory 'id' field.")
        elif not isinstance(ch_id, int):
            errors.append(f"Channel ID {ch_id!r} at index {idx} must be an integer, not {type(ch_id).__name__}.")
        else:
            if ch_id < PAESSLER_MIN_CHANNEL_ID or ch_id > PAESSLER_MAX_CHANNEL_ID:
                errors.append(
                    f"Channel ID {ch_id} violates Script v2 specification (Must be between {PAESSLER_MIN_CHANNEL_ID} and {PAESSLER_MAX_CHANNEL_ID})."
                )
            if ch_id in seen_ids:
                errors.append(f"Duplicate Channel ID detected: ID {ch_id} is defined multiple times.")
            seen_ids.add(ch_id)

        # Check Name & Value
        if "name" not in ch or not str(ch.get("name", "")).strip():
            errors.append(f"Channel with ID {ch.get('id', 'N/A')} missing non-empty 'name' attribute.")
        if "value" not in ch:
            errors.append(f"Channel '{ch.get('name', 'unnamed')}' (ID {ch.get('id', 'N/A')}) missing mandatory 'value' attribute.")
        elif not isinstance(ch.get("value"), (int, float)):
            errors.append(
                f"Channel '{ch.get('name')}' 'value' must be numeric (int/float), got {type(ch.get('value')).__name__}."
            )

    return (len(errors) == 0), errors, parsed


def print_diagnostic_report(success: bool, errors: List[str], parsed: Dict[str, Any]):
    """Emit formatted CLI validation report with commercial upgrade CTA."""
    print("=" * 70)
    print("  PRTG SCRIPT V2 SCHEMA VALIDATOR - DIAGNOSTIC REPORT")
    print("  Paessler PRTG 25.x.106+ Compliance Engine")
    print("=" * 70)

    if success:
        channels = parsed.get("channels", [])
        print("[+] STATUS: PASS - Fully Compliant with PRTG Script v2 Schema")
        print(f"[*] Channels Validated: {len(channels)}")
        print(f"[*] Root Status:        {parsed.get('status')}")
        print(f"[*] Message Payload:    {parsed.get('message', 'N/A')}")
        print("\nValidated Channels Summary:")
        for ch in channels:
            unit = ch.get("unit", ch.get("customunit", "Raw"))
            print(f"  - Channel {ch.get('id'):<4} | {ch.get('name'):<32} | Value: {ch.get('value')} ({unit})")
    else:
        print("[-] STATUS: FAIL - Sensor output will trigger PRTG parser errors")
        print(f"[*] Detected Violations: {len(errors)}\n")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}")

    print("\n" + "-" * 70)
    print("  Need production-hardened, zero-touch PRTG Script v2 sensors?")
    print("  - Fortinet FortiGate Enterprise Suite (IPsec SLA, SD-WAN, HA Drift, BGP)")
    print("  - pfSense High-Availability Suite (CARP VIPs, State Tables, pfBlockerNG)")
    print("  - Enterprise Switch Fabric Suite (Cisco IOS-XE / Huawei VRP DOM & CRC)")
    print("  Download ready-to-deploy suites: https://whop.com / https://lemonsqueezy.com")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="PRTG Script v2 JSON Schema Validator")
    parser.add_argument("--file", "-f", help="Path to JSON file containing sensor output")
    parser.add_argument("--exec", "-e", help="Command or script to execute and validate stdout")
    parser.add_argument("--self-test", action="store_true", help="Run internal validation test suite")

    args = parser.parse_args()

    raw_input_data = ""

    if args.self_test:
        test_payload = json.dumps({
            "version": 2,
            "status": "ok",
            "message": "Self-Test Verification",
            "channels": [
                {"id": 10, "name": "Ping RTT", "value": 15.2, "unit": "TimeResponse"},
                {"id": 11, "name": "Packet Loss", "value": 0, "unit": "Percent"}
            ]
        })
        success, errors, parsed = validate_v2_payload(test_payload)
        print_diagnostic_report(success, errors, parsed)
        sys.exit(0 if success else 1)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                raw_input_data = f.read()
        except Exception as exc:
            sys.stderr.write(f"Error reading file '{args.file}': {exc}\n")
            sys.exit(1)
    elif args.exec:
        try:
            proc = subprocess.run(args.exec, shell=True, capture_output=True, text=True, timeout=30)
            raw_input_data = proc.stdout
            if proc.returncode != 0:
                print(f"[!] Warning: Process exited with non-zero code {proc.returncode}")
                if proc.stderr:
                    print(f"[-] Stderr output: {proc.stderr.strip()}")
        except Exception as exc:
            sys.stderr.write(f"Execution failed for '{args.exec}': {exc}\n")
            sys.exit(1)
    else:
        # Read from stdin pipe
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(1)
        raw_input_data = sys.stdin.read()

    if not raw_input_data.strip():
        sys.stderr.write("Error: Received empty input. No data to validate.\n")
        sys.exit(1)

    success, errors, parsed = validate_v2_payload(raw_input_data)
    print_diagnostic_report(success, errors, parsed)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
