import subprocess

def run_command(command, description):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():    
    rg_name = "az104-04-rg1"
    vnet_name = "CoreServicesVnet"
    public_dns = "contoso-vasyl.com"
    private_dns = "private.contoso.com"

    cmd_pub = f"az network dns zone create --resource-group {rg_name} --name {public_dns}"
    run_command(cmd_pub, f"Створення публічної DNS-зони {public_dns}")

    cmd_priv = f"az network private-dns zone create --resource-group {rg_name} --name {private_dns}"
    run_command(cmd_priv, f"Створення приватної DNS-зони {private_dns}")

    cmd_link = f"az network private-dns link vnet create --resource-group {rg_name} --zone-name {private_dns} --name CoreServicesLink --virtual-network {vnet_name} --registration-enabled true"
    run_command(cmd_link, f"Прив'язка приватної зони до {vnet_name}")


if __name__ == "__main__":
    main()