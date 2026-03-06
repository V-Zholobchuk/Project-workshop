import subprocess

def run_command(command, description):
    print(f"⏳ Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-06-rg1"
    location = "swedencentral"
    vm_size = "Standard_D2s_v3"
    admin_user = "TestUser"
    admin_pass = "Pa$$w0rd12345678"

    run_command(f"az group create --name {rg_name} --location {location}", f"Створення ресурсної групи {rg_name}")

    run_command(f"az network vnet create --resource-group {rg_name} --name az104-06-vnet --address-prefix 10.60.0.0/16 --subnet-name subnet0 --subnet-prefix 10.60.0.0/24", "Створення VNet та підмережі subnet0")

    run_command(f"az network vnet subnet create --resource-group {rg_name} --vnet-name az104-06-vnet --name subnet1 --address-prefix 10.60.1.0/24", "Створення підмережі subnet1")
    run_command(f"az network vnet subnet create --resource-group {rg_name} --vnet-name az104-06-vnet --name subnet-appgw --address-prefix 10.60.3.224/27", "Створення підмережі для Application Gateway")

    run_command(f"az vm create --resource-group {rg_name} --name az104-06-vm0 --image Win2022Datacenter --vnet-name az104-06-vnet --subnet subnet0 --admin-username {admin_user} --admin-password {admin_pass} --size {vm_size} --public-ip-sku Standard --no-wait", "Створення az104-06-vm0 (запущено у фоні...)")
    
    run_command(f"az vm create --resource-group {rg_name} --name az104-06-vm1 --image Win2022Datacenter --vnet-name az104-06-vnet --subnet subnet1 --admin-username {admin_user} --admin-password {admin_pass} --size {vm_size} --public-ip-sku Standard", "Створення az104-06-vm1 (очікуйте...)")

    ps_iis_script = "Install-WindowsFeature -name Web-Server -IncludeManagementTools; Remove-Item C:\\inetpub\\wwwroot\\iisstart.htm; Add-Content -Path C:\\inetpub\\wwwroot\\iisstart.htm -Value $('Hello from ' + $env:computername)"
    
    run_command(f"az vm run-command invoke --resource-group {rg_name} --name az104-06-vm0 --command-id RunPowerShellScript --scripts \"{ps_iis_script}\"", "Встановлення IIS на az104-06-vm0")
    run_command(f"az vm run-command invoke --resource-group {rg_name} --name az104-06-vm1 --command-id RunPowerShellScript --scripts \"{ps_iis_script}\"", "Встановлення IIS на az104-06-vm1")


if __name__ == "__main__":
    main()