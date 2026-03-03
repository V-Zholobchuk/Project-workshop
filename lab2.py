import requests
import uuid
import time
from azure.identity import DefaultAzureCredential

GROUP_ID = "c1256084-4237-458d-a5fc-8dca61a997e7" 
MG_NAME = "az104-mg1"

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

    mg_scope = f"/providers/Microsoft.Management/managementGroups/{MG_NAME}"
    mg_url = f"{base_url}{mg_scope}?api-version=2020-05-01"
    
    mg_payload = {
        "name": MG_NAME,
        "properties": {
            "displayName": MG_NAME
        }
    }
    
    res = requests.put(mg_url, headers=headers, json=mg_payload)
    if res.status_code in [200, 201, 202]:
        print(f" {res.status_code}).")
    else:
        print(f"Error {res.text}")
        return
    time.sleep(20)

    vm_contributor_role_id = "9980e02c-c2be-4d73-94e8-173b1dc7cf3c" 
    assignment_uuid = str(uuid.uuid4())
    
    role_def_id = f"/providers/Microsoft.Authorization/roleDefinitions/{vm_contributor_role_id}"
    role_assign_url = f"{base_url}{mg_scope}/providers/Microsoft.Authorization/roleAssignments/{assignment_uuid}?api-version=2022-04-01"

    assign_payload = {
        "properties": {
            "roleDefinitionId": role_def_id,
            "principalId": GROUP_ID,
            "principalType": "Group"
        }
    }
    
    res_assign = requests.put(role_assign_url, headers=headers, json=assign_payload)
    if res_assign.status_code in [200, 201]:
        print("Роль успішно призначено")
    else:
        print(f"Помилка призначення ролі: {res_assign.text}")

    custom_role_uuid = str(uuid.uuid4())
    custom_role_url = f"{base_url}{mg_scope}/providers/Microsoft.Authorization/roleDefinitions/{custom_role_uuid}?api-version=2022-04-01"

    custom_role_payload = {
        "properties": {
            "roleName": "Custom Support Request",
            "description": "A custom contributor role for support requests",
            "assignableScopes": [mg_scope],
            "permissions": [
                {
                    "actions": [
                        "Microsoft.Resources/subscriptions/resourceGroups/read",
                        "Microsoft.Support/*"
                    ],
                    "notActions": [
                        "Microsoft.Support/register/action"
                    ],
                    "dataActions": [],
                    "notDataActions": []
                }
            ]
        }
    }
    res_custom = requests.put(custom_role_url, headers=headers, json=custom_role_payload)
    if res_custom.status_code in [200, 201]:
        print("Кастомну роль створено")
    else:
        print(f"Помилка створення ролі: {res_custom.text}")
if __name__ == "__main__":
    main()