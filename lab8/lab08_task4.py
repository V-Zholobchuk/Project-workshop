import subprocess

def run_command(command, description):
    print(f"Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"поимлка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-08-rg1"
    vmss_name = "vmss1"
    autoscale_name = "vmss1-autoscale"

    cmd_profile = (
        f"az monitor autoscale create --resource-group {rg_name} "
        f"--resource {vmss_name} --resource-type Microsoft.Compute/virtualMachineScaleSets "
        f"--name {autoscale_name} --min-count 1 --max-count 5 --count 2"
    )
    run_command(cmd_profile, "Створення профілю автомасштабування")

    cmd_scale_out = (
        f"az monitor autoscale rule create --resource-group {rg_name} --autoscale-name {autoscale_name} "
        f"--condition \"Percentage CPU > 75 avg 5m\" --scale out 1"
    )
    run_command(cmd_scale_out, "Додавання правила Scale Out ")

    cmd_scale_in = (
        f"az monitor autoscale rule create --resource-group {rg_name} --autoscale-name {autoscale_name} "
        f"--condition \"Percentage CPU < 25 avg 5m\" --scale in 1"
    )
    run_command(cmd_scale_in, "Додавання правила Scale In")


if __name__ == "__main__":
    main()