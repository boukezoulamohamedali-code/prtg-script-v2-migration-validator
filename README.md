# PRTG Script v2 JSON Schema Validator & Migration Pre-Flight CLI

Resolve Paessler PRTG 25.x.106+ Python Script Advanced Deprecation Tickets Without Runtime Crashes.

With the rollout of PRTG 25.x.106, Paessler deprecated the legacy Python Script Advanced sensor (CPython 3.4.2 / paepy) and mandated migration to the Script v2 Sensor architecture.

Migrating custom scripts to Script v2 introduces strict runtime constraints:
- Strict JSON Schema Validation: Channel IDs must be integers between 10 and 2,147,483,647, and total channels cannot exceed the 50-channel ceiling.
- Zero Stray Stdout Tolerance: Any stray print statement or unhandled traceback triggers JSON syntax_error at line 1 and column 1.
- -E Security Flag Isolation: PRTG invokes Python with -E, ignoring PYTHONPATH and python* environment variables.

## Quickstart: Validate Your Custom Sensor Before Deploying to PRTG

1. Run Internal Self-Test:
    python prtg_v2_schema_validator.py --self-test

2. Pipe Any Custom Sensor Script Output into the Validator:
    python my_custom_sensor.py | python prtg_v2_schema_validator.py

3. Validate a Saved JSON File:
    python prtg_v2_schema_validator.py --file sample_output.json

## Production-Hardened Enterprise PRTG Script v2 Suites

Skip writing, debugging, and maintaining custom MIBs and REST wrappers from scratch:
- Fortinet FortiGate Script v2 Suite ($199): IPsec VPN Phase-2 SLA, SD-WAN SLA Health across VDOMs, FGCP HA Cluster Sync Drift, BGP Neighbor & Prefix Monitor.
- pfSense HA & Security Script v2 Suite ($199): CARP Failover & Demotion Counter, Packet Filter State Table & MBUF Saturation, Multi-WAN dpinger SLA, pfBlockerNG & Suricata IPS Drops.
- Enterprise Switch Fabric & Migration Master Bundle ($499): Both Firewall Suites + Cisco IOS-XE & Huawei VRP Optical Transceiver DOM/DDM & Trunk CRC Sensors + prtg_v2_migrator.py Bulk CLI Migrator.

## Repository Topics
prtg-custom-sensor prtg-network-monitor python-networking fortigate pfsense cisco-ios-xe
