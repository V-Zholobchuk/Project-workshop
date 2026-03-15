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
    slot_name = "staging"
    repo_url = "https://github.com/Azure-Samples/php-docs-hello-world"
    branch = "master"

    cmd = (
        f"az webapp deployment source config --name {app_name} --resource-group {rg_name} "
        f"--slot {slot_name} --repo-url {repo_url} --branch {branch} --manual-integration"
    )
    print(f"https://{app_name}-{slot_name}.azurewebsites.net")

if __name__ == "__main__":
    main()