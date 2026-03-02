import requests
from azure.identity import DefaultAzureCredential

DOMAIN = "denisjurchuk1gmail.onmicrosoft.com" 
GUEST_EMAIL = "vasyl.zholobchuk.23@pnu.edu.ua"

def get_graph_headers():
    credential = DefaultAzureCredential()
    token = credential.get_token('https://graph.microsoft.com/.default').token
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

def main():
    headers = get_graph_headers()

    print("\nСтворюємо користувача")
    user_payload = {
        "accountEnabled": True,
        "displayName": "az104-user1",
        "mailNickname": "az104-user1",
        "userPrincipalName": f"az104-user1@{DOMAIN}",
        "passwordProfile": {
            "forceChangePasswordNextSignIn": False,
            "password": "StrongP@ssw0rd2026!"
        },
        "jobTitle": "IT Lab Administrator",
        "usageLocation": "US"
    }
    
    response = requests.post('https://graph.microsoft.com/v1.0/users', headers=headers, json=user_payload)
    if response.status_code == 201:
        user1_id = response.json().get('id')
        print(f"Користувача створено ID: {user1_id}")
    else:
        print(f"Помилка створення: {response.text}")
        return

    print(f"\n2. Надсилаємо запрошення для {GUEST_EMAIL}...")
    invite_payload = {
        "invitedUserEmailAddress": GUEST_EMAIL,
        "inviteRedirectUrl": "https://portal.azure.com",
        "sendInvitationMessage": True
    }
    
    response = requests.post('https://graph.microsoft.com/v1.0/invitations', headers=headers, json=invite_payload)
    if response.status_code == 201:
        guest_id = response.json().get('invitedUser', {}).get('id')
        print(f"Запрошення надіслано Guest ID: {guest_id}")
    else:
        print(f"Помилка запрошення: {response.text}")
        return


    group_payload = {
        "displayName": "IT Lab Administrators",
        "mailEnabled": False,
        "mailNickname": "ITLabAdmins",
        "securityEnabled": True
    }
    
    response = requests.post('https://graph.microsoft.com/v1.0/groups', headers=headers, json=group_payload)
    if response.status_code == 201:
        group_id = response.json().get('id')
        print(f"Групу створено Group ID: {group_id}")
    else:
        print(f"Помилка створення групи: {response.text}")
        return

    member_payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/users/{user1_id}"}
    req1 = requests.post(f'https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref', headers=headers, json=member_payload)
    
    guest_payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/users/{guest_id}"}
    req2 = requests.post(f'https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref', headers=headers, json=guest_payload)

    if req1.status_code == 204 and req2.status_code == 204:
        print("Користувача додано до групи")
    else:
        print("Помилка під час додавання до групи")

if __name__ == "__main__":
    main()