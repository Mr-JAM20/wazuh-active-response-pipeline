import json
import csv
import os

# 🎯 CONFIGURATION PARAMETERS
source_json = "C:/Users/lenovo/Desktop/python.py/JSON_PYTHON_READING/mass_vulnerabilities.json"
output_csv  = "C:/Users/lenovo/Desktop/python.py/JSON_PYTHON_READING/remediation_playbook.csv"

print("📊 [SECURITY ANALYTICS CORE] Actively compiling corporate infrastructure threat landscape...\n")

def process_mass_vulnerabilities():
    if not os.path.exists(source_json):
        print(f"❌ FILE MISSING: Target log asset could not be located at {source_json}")
        return

    # Ingest the entire structured database dump array list
    with open(source_json, "r") as file_stream:
        vuln_database = json.load(file_stream)
        
    print(f"📂 INGESTION SUCCESS: Loaded {len(vuln_database)} asset records into cache. Starting triage...\n")
    
    # 📝 INITIALIZE REPORT GENERATION LAYER: Prepare the output CSV stream with clean columns
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Write the executive header matrix
        writer.writerow(["TARGET_ASSET_NAME", "NETWORK_IP", "CVE_IDENTIFIER", "SEVERITY_LEVEL", "VULNERABILITY_TITLE"])
        
        critical_count = 0
        
        for record_node in vuln_database:
            source_block = record_node.get("_source", {})
            agent_info   = source_block.get("agent", {})
            vuln_info    = source_block.get("vulnerability", {})
            
            # Deep Safe Navigation extraction hooks
            asset_name = agent_info.get("name", "Unknown")
            asset_ip   = agent_info.get("ip", "Unknown")
            cve_id     = vuln_info.get("cve", "N/A")
            severity   = vuln_info.get("severity", "Medium")
            title      = vuln_info.get("title", "N/A")
            
            # 📊 ACTIONABLE FILTER GATEKEEPER: Isolate ONLY high-risk priority patch items
            if severity.lower() in ["high", "critical"]:
                print(f"⚠️ [HIGH RISK DISCOVERED] Target: {asset_name} | CVE: {cve_id} | Severity: {severity}")
                
                # Write the parsed columns natively to the hard disk reporting document
                writer.writerow([asset_name, asset_ip, cve_id, severity, title])
                critical_count += 1
                
    print(f"\n🔒 REPORT COMPILED SUCCESSFULLY: Filtered down to {critical_count} mission-critical patch targets.")
    print(f"📁 PLAYBOOK GENERATED AT LOCATION: {output_csv}")

if __name__ == "__main__":
    process_mass_vulnerabilities()
