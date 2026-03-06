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
    asg_name = "az104-04-asg1"
    nsg_name = "az104-04-nsg1"
    vnet_name = "CoreServicesVnet"
    subnet_name = "SharedServicesSubnet"

    cmd_asg = f"az network asg create --resource-group {rg_name} --name {asg_name} --location {location}"
    run_command(cmd_asg, "Створення Application Security Group (ASG)")

    cmd_nsg = f"az network nsg create --resource-group {rg_name} --name {nsg_name} --location {location}"
    run_command(cmd_nsg, "Створення Network Security Group (NSG)")

    cmd_assoc = f"az network vnet subnet update --resource-group {rg_name} --vnet-name {vnet_name} --name {subnet_name} --network-security-group {nsg_name}"
    run_command(cmd_assoc, f"Прив'язка NSG до підмережі {subnet_name}")

    cmd_inbound = f"az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name AllowASGTraffic --priority 100 --direction Inbound --access Allow --protocol Tcp --destination-port-ranges 80 --destination-asgs {asg_name}"
    run_command(cmd_inbound, "Створення вхідного правила (Inbound) для ASG")

    cmd_outbound = f"az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name DenyInternetOutbound --priority 100 --direction Outbound --access Deny --protocol Asterisk --destination-address-prefixes Internet"
    run_command(cmd_outbound, "Створення вихідного правила (Outbound) для заборони доступу до Інтернету")


if __name__ == "__main__":
    main()