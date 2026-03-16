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
    
    rg_name = "az104-11-rg1"
    vm_name = "az104-11-vm0"
    
    del_cmd = f"az vm delete --resource-group {rg_name} --name {vm_name} --yes --no-wait"
    run_command(del_cmd, f"Надсилання команди на видалення {vm_name}")
    
if __name__ == "__main__":
    main()