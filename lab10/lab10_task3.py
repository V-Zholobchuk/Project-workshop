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
    
    rg_name = "az104-10-rg1"
    vm_name = "az104-10-vm0"
    vault_name = "az104-10-rsv1"
    policy_name = "DefaultPolicy" 

    run_command(f"az vm wait --created --resource-group {rg_name} --name {vm_name}", "Очікування VM")

    backup_cmd = (
        f"az backup protection enable-for-vm --resource-group {rg_name} "
        f"--vault-name {vault_name} --vm {vm_name} --policy-name {policy_name}"
    )
    run_command(backup_cmd, f"Увімкнення бекапу для {vm_name}")


if __name__ == "__main__":
    main()