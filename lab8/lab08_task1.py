import subprocess

def run_command(command, description):
    print(f"Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-08-rg1"
    location = "swedencentral"
    vm_size = "Standard_D2s_v3"
    admin_user = "TestUser"
    admin_pass = "Pa$$w0rd12345678"

    run_command(f"az group create --name {rg_name} --location {location}", f"Створення групи {rg_name}")

    run_command(f"az network vnet create --resource-group {rg_name} --name az104-08-vnet1 --address-prefix 10.80.0.0/16 --subnet-name subnet0 --subnet-prefix 10.80.0.0/24", "Створення VNet та підмережі subnet0")

    cmd_vm1 = (
        f"az vm create --resource-group {rg_name} --name az104-vm1 "
        f"--image Win2022Datacenter --vnet-name az104-08-vnet1 --subnet subnet0 "
        f"--admin-username {admin_user} --admin-password {admin_pass} "
        f"--size {vm_size} --zone 1 --public-ip-sku Standard --no-wait"
    )
    run_command(cmd_vm1, "Створення az104-vm1 у Зоні 1")

    cmd_vm2 = (
        f"az vm create --resource-group {rg_name} --name az104-vm2 "
        f"--image Win2022Datacenter --vnet-name az104-08-vnet1 --subnet subnet0 "
        f"--admin-username {admin_user} --admin-password {admin_pass} "
        f"--size {vm_size} --zone 2 --public-ip-sku Standard"
    )
    run_command(cmd_vm2, "Створення az104-vm2 у Зоні 2")


if __name__ == "__main__":
    main()