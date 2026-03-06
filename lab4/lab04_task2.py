import json
import subprocess
import os

def create_json_files():
    template = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "vnetName": {"type": "string"},
            "location": {"type": "string"}
        },
        "resources": [
            {
                "type": "Microsoft.Network/virtualNetworks",
                "apiVersion": "2021-02-01",
                "name": "[parameters('vnetName')]",
                "location": "[parameters('location')]",
                "properties": {
                    "addressSpace": {
                        "addressPrefixes": ["10.30.0.0/16"]
                    },
                    "subnets": [
                        {
                            "name": "ManufacturingSystemSubnet",
                            "properties": {"addressPrefix": "10.30.10.0/24"}
                        },
                        {
                            "name": "SensorSubnet",
                            "properties": {"addressPrefix": "10.30.20.0/24"}
                        }
                    ]
                }
            }
        ]
    }

    parameters = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "vnetName": {"value": "ManufacturingVnet"},
            "location": {"value": "swedencentral"}
        }
    }

    with open('vnet_template.json', 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2)
    
    with open('vnet_parameters.json', 'w', encoding='utf-8') as f:
        json.dump(parameters, f, indent=2)
        

def deploy_template():
    rg_name = "az104-04-rg1"
    
    print(f"⏳ Відправляємо ARM-шаблон")
    cmd = f'az deployment group create --resource-group {rg_name} --template-file vnet_template.json --parameters "@vnet_parameters.json"'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Створено")
    else:
        print(f"помилка:\n{result.stderr}")

def main():
    create_json_files()
    deploy_template()

if __name__ == "__main__":
    main()