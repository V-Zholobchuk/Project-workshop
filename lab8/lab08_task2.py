import subprocess

def run_command(command, description):
    print(f"Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    elif "already exists" in result.stderr or "already attached" in result.stderr:
        print(f"Ресурс вже був створений\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-08-rg1"
    vm_name = "az104-vm1"
    disk_name = f"{vm_name}-datadisk1"
    
    sizes = ["Standard_B2s", "Standard_D4s_v3", "Standard_D2as_v4", "Standard_B2ms", "Standard_A2_v2"]
    
    resize_success = False
    for size in sizes:
        res = subprocess.run(f"az vm resize --resource-group {rg_name} --name {vm_name} --size {size}", shell=True, capture_output=True, text=True)
        
        if res.returncode == 0:
            resize_success = True
            break
        else:
            print(f"   -> Немає серверів для {size}")

    
    run_command(f"az vm disk attach --resource-group {rg_name} --vm-name {vm_name} --name {disk_name} --new --size-gb 128", f"Приєднання нового Data Disk (128 GB) до {vm_name}")

if __name__ == "__main__":
    main()