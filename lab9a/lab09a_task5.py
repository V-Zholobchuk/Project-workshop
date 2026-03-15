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
    plan_name = "az104-09a-plan" 
    autoscale_name = "az104-09a-autoscale"

    cmd_profile = (
        f"az monitor autoscale create --resource-group {rg_name} "
        f"--resource {plan_name} --resource-type Microsoft.Web/serverfarms "
        f"--name {autoscale_name} --min-count 1 --max-count 2 --count 1"
    )
    run_command(cmd_profile, "Створення профілю автомасштабування")

    cmd_scale_out = (
        f"az monitor autoscale rule create --resource-group {rg_name} --autoscale-name {autoscale_name} "
        f"--condition \"CpuPercentage > 70 avg 5m\" --scale out 1"
    )
    run_command(cmd_scale_out, "Додавання правила Scale Out ")
if __name__ == "__main__":
    main()