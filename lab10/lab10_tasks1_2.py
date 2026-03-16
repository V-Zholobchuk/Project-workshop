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
    location = "swedencentral"
    vm_name = "az104-10-vm0"
    vault_name = "az104-10-rsv1"
    vm_size = "Standard_D2as_v4" 

    run_command(f"az group create --name {rg_name} --location {location}", f"Створення групи {rg_name}")

    vm_cmd = (
        f"az vm create --resource-group {rg_name} --name {vm_name} "
        f"--image Win2022Datacenter --admin-username TestUser "
        f"--admin-password Pa$$w0rd12345678 --size {vm_size} "
        f"--public-ip-address \"\" --no-wait"
    )

    vault_cmd = f"az backup vault create --resource-group {rg_name} --name {vault_name} --location {location}"
    run_command(vault_cmd, f"Створення сховища {vault_name}")


if __name__ == "__main__":
    main()