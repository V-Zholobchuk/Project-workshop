import subprocess

def run_command(command, description):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-04-rg1"
    location = "swedencentral"
    vnet_name = "CoreServicesVnet"

    cmd_rg = f"az group create --name {rg_name} --location {location}"
    run_command(cmd_rg, "Створення ресурсної групи")

    cmd_vnet = f"az network vnet create --resource-group {rg_name} --name {vnet_name} --address-prefix 10.20.0.0/16 --subnet-name GatewaySubnet --subnet-prefix 10.20.0.0/27"
    run_command(cmd_vnet, "Створення CoreServicesVnet та GatewaySubnet")

    cmd_sub1 = f"az network vnet subnet create --resource-group {rg_name} --vnet-name {vnet_name} --name SharedServicesSubnet --address-prefixes 10.20.10.0/24"
    run_command(cmd_sub1, "Створення SharedServicesSubnet")

    cmd_sub2 = f"az network vnet subnet create --resource-group {rg_name} --vnet-name {vnet_name} --name DatabaseSubnet --address-prefixes 10.20.20.0/24"
    run_command(cmd_sub2, "Створення DatabaseSubnet")

    cmd_sub3 = f"az network vnet subnet create --resource-group {rg_name} --vnet-name {vnet_name} --name PublicWebServiceSubnet --address-prefixes 10.20.30.0/24"
    run_command(cmd_sub3, "Створення PublicWebServiceSubnet")


if __name__ == "__main__":
    main()