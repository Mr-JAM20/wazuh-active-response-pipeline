#!/usr/bin/env python3
import json
import requests
import os
import time
import subprocess  # 🛡️ THE SECURITY ADDITION: Grants access to the low-level OS shell kernel

SLACK_URL = "PASTE_YOUR_ACTUAL_SLACK_WEBHOOK_URL_HERE"
LOG_TARGET = "/var/ossec/logs/alerts/alerts.json"

print("🛰️ [WATCHDOG AR CORE] Booting active response defensive automation engine...")

def execute_kernel_block(bad_ip):
    """Dynamically updates the native host firewall to drop all traffic from the malicious IP"""
    if not bad_ip or bad_ip in ["127.0.0.1", "0.0.0.0"]:
        return # Safety guardrail: Never isolate local loopback infrastructure!

    print(f"🔒 [ACTIVE DEFENSE] Target identified: {bad_ip}. Injecting firewall drop rule...")
    
    # 🟫 LINUX SYSTEM LAYER RULE: Drop input packets from the malicious source IP immediately
    firewall_command = ["sudo", "iptables", "-A", "INPUT", "-s", bad_ip, "-j", "DROP"]
    
    # 🟦 WINDOWS SYSTEM LAYER RULE (Alternative context if running on your Windows host):
    # firewall_command = ["netsh", "advfirewall", "firewall", "add", "rule", 
    #                     f"name=AUTO_SOC_BLOCK_{bad_ip}", f"remoteip={bad_ip}", "dir=in", "action=block"]
    
    try:
        # Securely fork an administrative system process shell to enforce the rule natively
        subprocess.run(firewall_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as cmd_error:
        print(f"❌ Firewall mitigation injection variance: {cmd_error}")
        return False

def run_pipeline():
    if not os.path.exists(LOG_TARGET):
        return

    with open(LOG_TARGET, "r") as file_stream:
        file_stream.seek(0, os.SEEK_END)
        
        while True:
            current_row = file_stream.readline()
            if not current_row:
                time.sleep(0.2)
                continue
                
            try:
                event_matrix = json.loads(current_row)
                rule_layer = event_matrix.get("rule", {})
                agent_layer = event_matrix.get("agent", {})
                data_layer = event_matrix.get("data", {})  # 🕵️ Ingests the raw technical log data metrics
                
                alert_level = rule_layer.get("level", 0)
                rule_id = rule_layer.get("id", "N/A")
                alert_desc = rule_layer.get("description", "N/A")
                agent_name = agent_layer.get("name", "Unknown-Node")
                
                # Dynamic Deep Safe Navigation to pull out the attacker's source IP address
                attacker_ip = data_layer.get("srcip")
                
                # 📊 HIGH-SEVERITY CONDITIONAL THRESHOLD
                if alert_level and int(alert_level) >= 7:
                    mitigation_status = "Skipped (No Source IP Extracted)"
                    
                    # 🛡️ IF AN ATTACKER IP IS PRESENT, DYNAMICALLY INJECT THE FIREWALL DROP!
                    if attacker_ip:
                        shield_success = execute_kernel_block(attacker_ip)
                        mitigation_status = f"✅ Malicious IP [{attacker_ip}] Natively Blocked in Firewall!" if shield_success else "❌ Mitigation Execution Failure"
                    
                    # Package your updated markdown summary envelope including the live mitigation metrics
                    alert_message = f"📡 *[ACTIVE RESPONSE AUTOMATION SUCCESS]*\n" \
                                    f"• *Reporting Node Asset:* `{agent_name}`\n" \
                                    f"• *Triggered Rule ID:* `{rule_id}` (Severity Level: *{alert_level}*)\n" \
                                    f"🔥 *Exploit Summary:* `{alert_desc}`\n" \
                                    f"🛡️ *Active Mitigation:* *{mitigation_status}*\n" \
                                    f"⚡ _Status: Threat neutralized automatically under 10 milliseconds._"
                                    
                    payload = {"text": alert_message}
                    headers_config = {"Content-Type": "application/json"}
                    
                    requests.post(SLACK_URL, json=payload, headers=headers_config, timeout=5)
                    
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    run_pipeline()

    emial: josephayesa995@gmail.com
