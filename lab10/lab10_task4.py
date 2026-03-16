import subprocess
import json
import os

def run_command(command, description):
    print(f"Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
        return result.stdout.strip()
    else:
        print(f"помилка:\n{result.stderr}\n")
        return None

def main():
    
    rg_name = "az104-10-rg1"
    location = "swedencentral"
    vault_name = "az104-10-rsv1"
    law_name = "az104-10-law1"
    
    run_command(f"az monitor log-analytics workspace create --resource-group {rg_name} --workspace-name {law_name} --location {location}", f"Перевірка Log Analytics Workspace ({law_name})")
    
    vault_id = run_command(f"az backup vault show --name {vault_name} --resource-group {rg_name} --query id -o tsv", "Отримання ID Recovery Services Vault")
    law_id = run_command(f"az monitor log-analytics workspace show --resource-group {rg_name} --workspace-name {law_name} --query id -o tsv", "Отримання ID Log Analytics Workspace")
    
    if vault_id and law_id:
        logs_config = [{"categoryGroup": "allLogs", "enabled": True}]
        metrics_config = [{"category": "AllMetrics", "enabled": True}] 
        
        with open('logs.json', 'w') as f:
            json.dump(logs_config, f)
        with open('metrics.json', 'w') as f:
            json.dump(metrics_config, f)
            
        diag_cmd = (
            f"az monitor diagnostic-settings create --name vault-diag "
            f"--resource {vault_id} --workspace {law_id} "
            f"--logs @logs.json --metrics @metrics.json"
        )
        run_command(diag_cmd, "Налаштування Diagnostic Settings для надсилання логів")
        
        if os.path.exists('logs.json'): os.remove('logs.json')
        if os.path.exists('metrics.json'): os.remove('metrics.json')
        

if __name__ == "__main__":
    main()