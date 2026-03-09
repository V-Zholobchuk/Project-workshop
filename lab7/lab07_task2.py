import subprocess
import json
import datetime

def run_command(command, description):
    print(f"перевірка {description}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працює\n")
        return result.stdout.strip()
    else:
        print(f"помилка\n{result.stderr}\n")
        return None

def get_account_key(rg_name, account_name):
    cmd = f"az storage account keys list -g {rg_name} -n {account_name} -o json"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            keys = json.loads(result.stdout)
            print(f"є\n")
            return keys[0]['value'] 
        except json.JSONDecodeError:
            print(f"ПОМИЛКА: Не вдалося розпарсити JSON.\n")
            return None
    else:
        print(f"помилка\n{result.stderr}\n")
        return None

def main():
    
    rg_name = "az104-07-rg1"
    account_name = "az104stor06548" 
    container_name = "az104-07-container"
    blob_name = "test_blob.txt"

    account_key = get_account_key(rg_name, account_name)
    if not account_key:
        return

    run_command(f"az storage container create --name {container_name} --account-name {account_name} --account-key {account_key}", f"створення контейнера '{container_name}'")

    with open(blob_name, "w", encoding="utf-8") as f:
        f.write("Hello")

    run_command(f"az storage blob upload --account-name {account_name} --account-key {account_key} --container-name {container_name} --name {blob_name} --file {blob_name}", f"Завантаження файлу '{blob_name}' у контейнер")

    expiry = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%MZ')
    
    sas_token = run_command(f"az storage blob generate-sas --account-name {account_name} --account-key {account_key} --container-name {container_name} --name {blob_name} --permissions r --expiry {expiry} -o tsv")

    if sas_token:
        sas_token = sas_token.strip('"\n\r ')
        blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
        
        print(f"{blob_url}")

if __name__ == "__main__":
    main()