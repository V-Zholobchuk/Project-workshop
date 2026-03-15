import subprocess

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
    
    rg_name = "az104-09c-rg1"
    location = "swedencentral" 
    env_name = "my-environment"
    app_name = "my-app"
    image = "mcr.microsoft.com/k8se/quickstart:latest"

    run_command("az extension add --name containerapp --upgrade", "")
    
    run_command("az provider register --namespace Microsoft.App --wait", "Реєстрація провайдера Microsoft.App ")
    run_command("az provider register --namespace Microsoft.OperationalInsights --wait", "Реєстрація провайдера логів")

    run_command(f"az group create --name {rg_name} --location {location}", f"Створення групи {rg_name}")

    env_cmd = f"az containerapp env create --name {env_name} --resource-group {rg_name} --location {location}"
    run_command(env_cmd, f"Створення Container Apps Environment ({env_name})")

    app_cmd = (
        f"az containerapp create --name {app_name} --resource-group {rg_name} "
        f"--environment {env_name} --image {image} "
        f"--target-port 80 --ingress external"
    )
    run_command(app_cmd, f"Розгортання Container App ({app_name}) з образом Hello World")

    fqdn_cmd = f"az containerapp show --name {app_name} --resource-group {rg_name} --query properties.configuration.ingress.fqdn -o tsv"
    fqdn = run_command(fqdn_cmd, "Отримання публічної адреси додатку")

    if fqdn:
        print(f"https://{fqdn}")

if __name__ == "__main__":
    main()