import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"прпацює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-05-rg1b"
    rt_name = "az104-05-rt1"
    route_name = "az104-05-route-vnet1"
    
    cmd_rt = f"az network route-table create --resource-group {rg_name} --name {rt_name} --location swedencentral"
    run_command(cmd_rt, f"Створення таблиці маршрутизації: {rt_name}")

    cmd_route = f"az network route-table route create --resource-group {rg_name} --route-table-name {rt_name} --name {route_name} --address-prefix 10.20.20.0/24 --next-hop-type VirtualAppliance --next-hop-ip-address 10.20.10.4"
    run_command(cmd_route, f"Створення кастомного маршруту: {route_name}")

    cmd_assoc = f"az network vnet subnet update --resource-group {rg_name} --vnet-name ManufacturingVnet --name ManufacturingSubnet --route-table {rt_name}"
    run_command(cmd_assoc, "Прив'язка таблиці маршрутизації до підмережі ManufacturingSubnet")

if __name__ == "__main__":
    main()