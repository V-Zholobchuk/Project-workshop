import subprocess
import json

def run_command(command, description):
    print(f"⏳ Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def get_json_output(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

def main():
    
    rg_name = "az104-06-rg1"
    lb_name = "az104-06-lb4"
    pip_name = "az104-06-pip4"
    
    run_command(f"az network public-ip create --resource-group {rg_name} --name {pip_name} --sku Standard", f"Створення Public IP: {pip_name}")
    
    run_command(f"az network lb create --resource-group {rg_name} --name {lb_name} --sku Standard --public-ip-address {pip_name} --frontend-ip-name myFrontEnd --backend-pool-name myBackEndPool", f"Створення Load Balancer: {lb_name}")
    
    run_command(f"az network lb probe create --resource-group {rg_name} --lb-name {lb_name} --name myHealthProbe --protocol tcp --port 80", "Створення Health Probe (TCP порт 80)")
    
    run_command(f"az network lb rule create --resource-group {rg_name} --lb-name {lb_name} --name myHTTPRule --protocol tcp --frontend-port 80 --backend-port 80 --frontend-ip-name myFrontEnd --backend-pool-name myBackEndPool --probe-name myHealthProbe --disable-outbound-snat true", "Створення правила балансування (Port 80 -> 80)")
    
    servers = ["az104-06-vm0", "az104-06-vm1"]
    for vm in servers:
        print(f"🔍 Аналіз конфігурації мережі для {vm}...")
        
        vm_info = get_json_output(f"az vm show -g {rg_name} -n {vm}")
        if vm_info and 'networkProfile' in vm_info:
            nic_id = vm_info['networkProfile']['networkInterfaces'][0]['id']
            nic_name = nic_id.split('/')[-1]
            
            nic_info = get_json_output(f"az network nic show -g {rg_name} -n {nic_name}")
            if nic_info and 'ipConfigurations' in nic_info:
                ipconf_name = nic_info['ipConfigurations'][0]['name']
                
                run_command(f"az network nic ip-config address-pool add --address-pool myBackEndPool --ip-config-name {ipconf_name} --nic-name {nic_name} --resource-group {rg_name} --lb-name {lb_name}", f"Підключення {vm} (NIC: {nic_name}) до Backend Pool")
            else:
                print(f"не вдалося отримати IP-конфігурацію для {nic_name}\n")
        else:
            print(f"не вдалося знайти інформацію про мережу для {vm}\n")


if __name__ == "__main__":
    main()