# EWOS Autonomous B2B Outbound Engineering Playbook
## Target Vertical: MSP Technical Directors, Senior SysAdmins, Infrastructure Leads

---

### Touch 1 (Day 1): The Deprecation Fix / Technical Utility
**Subject:** PRTG 25.x Script v2 migration / FortiOS & pfSense sensors
**Body:**
Hi {{first_name}},

Noticed your team manages {{vendor_focus}} infrastructure. If you've updated PRTG to version 25.x recently, you likely have an active administrative to-do ticket regarding the deprecation of the legacy Python Script Advanced sensor (CPython 3.4 / paepy).

We open-sourced a small pre-flight validator CLI on GitHub that checks custom sensor outputs against Paessler's Script v2 JSON schema and flags the -E flag / environment isolation issues before they trigger line 1 JSON syntax errors:
https://github.com/{{your_github_username}}/prtg-script-v2-migration-validator

If your engineers don't want to spend time rebuilding custom MIBs or REST API polling from scratch, we also maintain production-hardened, ready-to-deploy Script v2 suites for Fortinet (IPsec SLA, SD-WAN health, HA sync drift) and pfSense (CARP failovers, state table saturation):
https://lemonsqueezy.com/your-store

Best,
{{your_name}}
Network Systems Engineer

---

### Touch 2 (Day 4): The Asynchronous Firewall Hardening Audit
**Subject:** Offline CIS & VLAN boundary audit for {{company_name}}
**Body:**
Hi {{first_name}},

Quick follow-up. For MSPs and teams managing perimeter firewalls (FortiGate / pfSense), staying ahead of annual cyber-insurance renewal requirements usually means auditing rulebases for shadowed policies and inter-VLAN boundary leaks.

We operate an automated, offline static configuration audit engine. Your team strips passwords locally using our 10-line sanitization script, uploads the raw config.xml or .conf file, and receives an executive compliance PDF mapped to CIS Benchmarks within 2 hours:
- Posture score (0-100)
- Any-to-Any wildcard inter-VLAN rule identification
- Shadowed policy detection
- Ready-to-paste CLI remediation blocks

No discovery calls or vendor onboarding required ($400 flat):
https://whop.com/your-store

Sample audit report attached for reference.

Best,
{{your_name}}

---

### Touch 3 (Day 9): Final Technical Follow-Up
**Subject:** PRTG sensor migration tool + bulk CLI
**Body:**
Hi {{first_name}},

Closing the loop here. If your team is handling a larger PRTG environment with dozens of deprecated custom sensors, our bulk migration CLI scans your PRTG Core via API, maps legacy sensors directly to Script v2 equivalents, and verifies probe compatibility.

Full details and technical documentation are available here:
https://lemonsqueezy.com/your-store

Best regards,
{{your_name}}
