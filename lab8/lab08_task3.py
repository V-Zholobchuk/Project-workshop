import subprocess

def run_command(command, description):
    print(f"Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-08-rg1"
    vmss_name = "vmss1"
    vm_size = "Standard_D2as_v4" 
    admin_user = "TestUser"
    admin_pass = "Pa$$w0rd12345678"

    
    cmd_vmss = (
        f"az vmss create "
        f"--resource-group {rg_name} "
        f"--name {vmss_name} "
        f"--image Win2022Datacenter "
        f"--vm-sku {vm_size} "
        f"--instance-count 2 "
        f"--admin-username {admin_user} "
        f"--admin-password {admin_pass} "
        f"--zones 1 2 3 "
        f"--orchestration-mode Uniform " 
        f"--disable-overprovision "
        f"--upgrade-policy-mode Automatic"
    )
    
    run_command(cmd_vmss, f"Розгортання масштабованого набору {vmss_name} у зонах 1 2 3")


if __name__ == "__main__":
    main()