import subprocess
import time

def run_command(command, description):
    print(f"⏳ Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"помилка\n{result.stderr}\n")

def get_output(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    
    rg_name = "az104-06-rg1"
    appgw_name = "az104-06-appgw5"
    pip_name = "az104-06-pip5"
    vnet_name = "az104-06-vnet"
    subnet_name = "subnet-appgw"
    
    ip_vm0 = get_output(f"az vm show -d -g {rg_name} -n az104-06-vm0 --query privateIps -o tsv")
    ip_vm1 = get_output(f"az vm show -d -g {rg_name} -n az104-06-vm1 --query privateIps -o tsv")
    
    if not ip_vm0 or not ip_vm1:
        return
        
    print(f"✅ Знайдено IP: az104-06-vm0 ({ip_vm0}), az104-06-vm1 ({ip_vm1})\n")

    run_command(f"az network public-ip create --resource-group {rg_name} --name {pip_name} --sku Standard --allocation-method Static", f"Створення Public IP: {pip_name}")
    
    appgw_cmd = (
        f"az network application-gateway create "
        f"--resource-group {rg_name} "
        f"--name {appgw_name} "
        f"--sku Standard_v2 "
        f"--capacity 2 "
        f"--vnet-name {vnet_name} "
        f"--subnet {subnet_name} "
        f"--public-ip-address {pip_name} "
        f"--servers {ip_vm0} {ip_vm1} "
        f"--frontend-port 80 "
        f"--http-settings-port 80 "
        f"--http-settings-protocol Http "
        f"--priority 100"
    )
    
    
    print("⏳ Отримання IP-адреси Application Gateway")
    appgw_ip = get_output(f"az network public-ip show --resource-group {rg_name} --name {pip_name} --query ipAddress -o tsv")
    
    print(f"http://{appgw_ip}")

if __name__ == "__main__":
    main()