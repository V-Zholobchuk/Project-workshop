import subprocess
import random
import string

def run_command(command, description):
    print(f"перевірка: {description}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
        return result.stdout.strip()
    else:
        print(f"помилка:\n{result.stderr}\n")
        return None

def main():    
    rg_name = "az104-07-rg1"
    location = "swedencentral"
    
    random_suffix = ''.join(random.choices(string.digits, k=5))
    storage_account_name = f"az104stor{random_suffix}"
    
    run_command(f"az group create --name {rg_name} --location {location}", f"Створення групи {rg_name}")
    
    cmd_create_sa = (
        f"az storage account create "
        f"--name {storage_account_name} "
        f"--resource-group {rg_name} "
        f"--location {location} "
        f"--sku Standard_LRS "
        f"--kind StorageV2 "
        f"--allow-blob-public-access true" 
    )
    
    print(f"Згенероване ім'я сховища {storage_account_name}")
    run_command(cmd_create_sa, f"Створення Storage Account ({storage_account_name})")
    
if __name__ == "__main__":
    main()