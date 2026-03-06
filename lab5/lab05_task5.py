import subprocess
import json

def run_command(command, description):
    print(f"Виконується: {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            output_json = json.loads(result.stdout)
            print(f"Результат із віртуальної машини:\n{output_json['value'][0]['message']}")
        except:
            print(result.stdout)
    else:
        print(f"помилка:\n{result.stderr}\n")

def main():
    
    rg_name = "az104-05-rg1b"
    vm_name = "ManufacturingVM"
    target_ip = "10.20.20.4" 
    
    ps_script = f"Test-NetConnection {target_ip} -Port 3389"    
    cmd_run = f"az vm run-command invoke --resource-group {rg_name} --name {vm_name} --command-id RunPowerShellScript --scripts \"{ps_script}\""
    
    run_command(cmd_run, f"Запуск Test-NetConnection з {vm_name} до {target_ip}")
if __name__ == "__main__":
    main()