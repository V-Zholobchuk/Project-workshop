import requests
from azure.identity import DefaultAzureCredential

def get_arm_headers():
    credential = DefaultAzureCredential()
    token = credential.get_token('https://management.azure.com/.default').token
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

def main():
    headers = get_arm_headers()
    base_url = "https://management.azure.com"

    sub_res = requests.get(f"{base_url}/subscriptions?api-version=2020-01-01", headers=headers)
    if sub_res.status_code == 200 and len(sub_res.json().get('value', [])) > 0:
        sub_id = sub_res.json()['value'][0]['subscriptionId']
        print(f"Підписку знайдено: {sub_id}")
    else:
        print("Підписку не знайдено")
        return

    rg_name = "az104-02b-rg1"
    rg_scope = f"/subscriptions/{sub_id}/resourcegroups/{rg_name}"

    rg_url = f"{base_url}{rg_scope}?api-version=2021-04-01"
    rg_payload = {
        "location": "eastus",
        "tags": {
            "Cost Center": "000"
        }
    }
    
    res = requests.put(rg_url, headers=headers, json=rg_payload)
    if res.status_code in [200, 201]:
        print("Resource Group з тегом створено")
    else:
        print(f"Помилка створення RG: {res.text}")
        return

    print("\n2. Призначаємо політику 'Inherit a tag from the resource group if missing'...")
    policy_def_id = "/providers/Microsoft.Authorization/policyDefinitions/ea3f2387-9b95-492a-a190-fcdc54f7b070"
    policy_assign_name = "inherit-tag-policy"
    policy_url = f"{base_url}{rg_scope}/providers/Microsoft.Authorization/policyAssignments/{policy_assign_name}?api-version=2024-04-01"
    policy_payload = {
        "properties": {
            "displayName": "Inherit Cost Center tag",
            "policyDefinitionId": policy_def_id,
            "parameters": {
                "tagName": {
                    "value": "Cost Center"
                }
            }
        },
        "identity": {
            "type": "SystemAssigned"
        },
        "location": "eastus"
    }

    res = requests.put(policy_url, headers=headers, json=policy_payload)
    if res.status_code in [200, 201]:
        print("Політику призначено")
    else:
        print(f"Помилка: {res.text}")

    print("\n3. Встановлюємо Delete Lock на ресурсну групу")
    lock_name = "PreventDeleteLock"
    lock_url = f"{base_url}{rg_scope}/providers/Microsoft.Authorization/locks/{lock_name}?api-version=2020-05-01"

    lock_payload = {
        "properties": {
            "level": "CanNotDelete",
            "notes": "Prevent accidental deletion of the resource group"
        }
    }

    res = requests.put(lock_url, headers=headers, json=lock_payload)
    if res.status_code in [200, 201]:
        print("Resource Lock створено")
    else:
        print(f"Помилка: {res.text}")

if __name__ == "__main__":
    main()