import subprocess

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
    
    rg_name = "az104-11-rg1"
    rule_name = "Maintenance_Suppress_Rule"
    
    rg_id = run_command(f"az group show --name {rg_name} --query id --output tsv")
    if not rg_id: return
    
    rule_cmd = (
        f'az monitor alert-processing-rule create '
        f'--name {rule_name} --resource-group {rg_name} '
        f'--scopes {rg_id} --rule-type RemoveAllActionGroups '
        f'--description "Suppress alerts during scheduled maintenance"'
    )
    run_command(rule_cmd, f"Створення правила '{rule_name}'")
    

if __name__ == "__main__":
    main()