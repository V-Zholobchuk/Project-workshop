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
    location = "swedencentral"
    vm_name = "az104-11-vm0"
    
    run_command(f"az group create --name {rg_name} --location {location}", f"Перевірка групи {rg_name}")
    
    vm_cmd = (
        f"az vm create --resource-group {rg_name} --name {vm_name} --location {location} "
        f"--image Ubuntu2204 --admin-username azureuser --generate-ssh-keys "
        f"--public-ip-address \"\" --size Standard_D2as_v4" 
    )
    run_command(vm_cmd, f"Розгортання віртуальної машини {vm_name} (Standard_D2as_v4)")
    

if __name__ == "__main__":
    main()  