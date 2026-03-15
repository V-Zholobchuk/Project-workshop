import subprocess

def run_command(command, description):
    print(f"Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():    
    rg_name = "az104-09a-rg1"
    app_name = "az104-webapp-34923" 

    cmd = f"az webapp deployment slot swap --resource-group {rg_name} --name {app_name} --slot staging --target-slot production"
    

    print(f"https://{app_name}.azurewebsites.net")

if __name__ == "__main__":
    main()