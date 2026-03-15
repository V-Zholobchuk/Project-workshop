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
    
    rg_name = "az104-09a-rg1"
    location = "swedencentral" 
    plan_name = "az104-09a-plan"
    
    random_suffix = ''.join(random.choices(string.digits, k=5))
    app_name = f"az104-webapp-{random_suffix}"
    
    run_command(f"az group create --name {rg_name} --location {location}", f"Створення групи {rg_name}")

    run_command(f"az appservice plan create --name {plan_name} --resource-group {rg_name} --location {location} --sku S1 --is-linux", "Створення App Service Plan")

    print(f"ім'я сайту: {app_name}")
    run_command(f"az webapp create --resource-group {rg_name} --plan {plan_name} --name {app_name} --runtime \"PHP|8.2\"", f"Створення Web App ({app_name})")

    run_command(f"az webapp deployment slot create --name {app_name} --resource-group {rg_name} --slot staging", "Створення слота розгортання 'staging'")

    print(f"основний сайт:https://{app_name}.azurewebsites.net")
    print(f"тестовий сайт:https://{app_name}-staging.azurewebsites.net")

if __name__ == "__main__":
    main()