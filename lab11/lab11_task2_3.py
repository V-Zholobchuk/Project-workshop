import subprocess

def run_command(command, description):
    print(f"Виконується: {description}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
        return result.stdout.strip()
    else:
        print(f"помилка:\n{result.stderr}\n")
        return None

def main():
    
    email_address = "vasyl.zholobchuk.23@pnu.edu.ua"
    
    rg_name = "az104-11-rg1"
    vm_name = "az104-11-vm0"
    ag_name = "EmailActionGroup"
    alert_name = "Delete_VM_Alert"


    vm_id = run_command(f"az vm show --resource-group {rg_name} --name {vm_name} --query id --output tsv")
    if not vm_id: return

    ag_cmd = f'az monitor action-group create --resource-group {rg_name} --name {ag_name} --short-name EmailAG --action email SendEmailToMe {email_address}'
    run_command(ag_cmd, f"Створення групи дій {email_address}")

    ag_id = run_command(f"az monitor action-group show --resource-group {rg_name} --name {ag_name} --query id --output tsv")
    if not ag_id: return

    condition = "category=Administrative and operationName=Microsoft.Compute/virtualMachines/delete"
    alert_cmd = f'az monitor activity-log alert create --resource-group {rg_name} --name {alert_name} --scope {vm_id} --condition {condition} --action-group {ag_id}'
    run_command(alert_cmd, f"Створення правила'{alert_name}'")

if __name__ == "__main__":
    main()