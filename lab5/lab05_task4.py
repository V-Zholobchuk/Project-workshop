import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-05-rg1b" 

    cmd_peer1 = f"az network vnet peering create --resource-group {rg_name} --name CoreToManufacturing --vnet-name CoreServicesVnet --remote-vnet ManufacturingVnet --allow-vnet-access"
    run_command(cmd_peer1, "Створення пірингу: CoreServicesVnet ---> ManufacturingVnet")

    cmd_peer2 = f"az network vnet peering create --resource-group {rg_name} --name ManufacturingToCore --vnet-name ManufacturingVnet --remote-vnet CoreServicesVnet --allow-vnet-access"
    run_command(cmd_peer2, "Створення зворотного пірингу: ManufacturingVnet ---> CoreServicesVnet")
if __name__ == "__main__":
    main()