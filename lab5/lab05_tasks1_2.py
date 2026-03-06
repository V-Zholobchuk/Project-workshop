import subprocess

def run_command(command, description):
    print(f"⏳ Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():    
    rg_name = "az104-05-rg1b"
    location = "swedencentral"
    admin_user = "TestUser"
    admin_pass = "Pa$$w0rd12345678"
    vm_size = "Standard_D2s_v3" 

    cmd_rg = f"az group create --name {rg_name} --location {location}"
    run_command(cmd_rg, f"Створення ресурсної групи {rg_name}")

    cmd_vnet1 = f"az network vnet create --resource-group {rg_name} --name CoreServicesVnet --address-prefix 10.20.0.0/16 --subnet-name CoreServicesSubnet --subnet-prefix 10.20.20.0/24"
    run_command(cmd_vnet1, "Створення CoreServicesVnet (10.20.0.0/16)")

    cmd_vm1 = f"az vm create --resource-group {rg_name} --name CoreServicesVM --image Win2022Datacenter --vnet-name CoreServicesVnet --subnet CoreServicesSubnet --admin-username {admin_user} --admin-password {admin_pass} --size {vm_size} --public-ip-sku Standard --no-wait"
    run_command(cmd_vm1, f"Створення CoreServicesVM (розмір: {vm_size}, у фоні...)")

    cmd_vnet2 = f"az network vnet create --resource-group {rg_name} --name ManufacturingVnet --address-prefix 10.30.0.0/16 --subnet-name ManufacturingSubnet --subnet-prefix 10.30.10.0/24"
    run_command(cmd_vnet2, "Створення ManufacturingVnet (10.30.0.0/16)")

    cmd_vm2 = f"az vm create --resource-group {rg_name} --name ManufacturingVM --image Win2022Datacenter --vnet-name ManufacturingVnet --subnet ManufacturingSubnet --admin-username {admin_user} --admin-password {admin_pass} --size {vm_size} --public-ip-sku Standard"
    run_command(cmd_vm2, f"Створення ManufacturingVM (розмір: {vm_size}, очікуйте...)")


if __name__ == "__main__":
    main()