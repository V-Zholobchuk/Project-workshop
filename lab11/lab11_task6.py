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
    
    rg_name = "az104-11-rg1"
        
    log_cmd = (
        f'az monitor activity-log list '
        f'--resource-group {rg_name} --max-events 10 '
        f'--query "[].{{Time:eventTimestamp, Operation:operationName.localizedValue, Status:status.localizedValue}}" '
        f'--output table'
    )
    
    logs = run_command(log_cmd)
    
    if logs:
        print("-" * 70)
        print(logs)
        print("-" * 70)
        

if __name__ == "__main__":
    main()