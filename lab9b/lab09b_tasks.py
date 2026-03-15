import subprocess
import random
import string

def run_command(command, description):
    print(f"Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
        return result.stdout.strip()
    else:
        print(f"помилка:\n{result.stderr}\n")
        return None

def main():
    
    rg_name = "az104-09b-rg1"
    location = "swedencentral"
    container_name = "az104-c1"
    image = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    dns_name_label = f"az104-c1-{random_suffix}"

    run_command(f"az group create --name {rg_name} --location {location}", f"Створення групи {rg_name}")

    cmd_create_aci = (
        f"az container create --resource-group {rg_name} "
        f"--name {container_name} --image {image} "
        f"--dns-name-label {dns_name_label} --ports 80 "
        f"--os-type Linux "
        f"--cpu 1 --memory 1.5" 
    )
    run_command(cmd_create_aci, "Розгортання Docker-контейнера в ACI")

    fqdn_cmd = f"az container show --resource-group {rg_name} --name {container_name} --query ipAddress.fqdn -o tsv"
    fqdn = run_command(fqdn_cmd, "Отримання публічної адреси контейнера (FQDN)")

    print(f"http://{fqdn}")

if __name__ == "__main__":
    main()