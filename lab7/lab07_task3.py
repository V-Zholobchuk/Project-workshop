import subprocess
import json

def run_command(command, description):
    print(f"перевірка {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"працюж\n")
        return result.stdout.strip()
    else:
        print(f"помилка:\n{result.stderr}\n")
        return None

def get_account_key(rg_name, account_name):
    cmd = f"az storage account keys list -g {rg_name} -n {account_name} -o json"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            keys = json.loads(result.stdout)
            return keys[0]['value']
        except:
            return None
    return None

def main():
    
    rg_name = "az104-07-rg1"
    account_name = "az104stor06548" 
    share_name = "az104-07-share"
    file_name = "shared_test_file.txt"

    account_key = get_account_key(rg_name, account_name)
    if not account_key:
        print("Не вдалося отримати ключ.")
        return
    print("є\n")

    run_command(f"az storage share create --name {share_name} --account-name {account_name} --account-key {account_key} --quota 1", f"Створення File Share '{share_name}'")

    with open(file_name, "w") as f:
        f.write("hi")
    print(f"файл {file_name} створено.\n")

    run_command(f"az storage file upload --share-name {share_name} --source {file_name} --account-name {account_name} --account-key {account_key}", f"Завантаження '{file_name}' у папку")

    print("gеревірка вмісту папки")
    files_list = run_command(f"az storage file list --share-name {share_name} --account-name {account_name} --account-key {account_key} -o table", "отримання списку файлів")
    
    if files_list:
        print(f"Вміст папки '{share_name}':\n")
        print(files_list)
        
if __name__ == "__main__":
    main()