import os
import subprocess
from datetime import datetime
import re

class VMCreation:
    def __init__(self):
        self.azure_conf_file = "azure.conf"
        self.gcp_conf_file = "gcp.conf"

    def validate_config(self, vm_details, config_type):
        if config_type == 'azure':
            required_variables = ['name', 'resource-group', 'image', 'location', 'admin-username']
        elif config_type == 'GCP':
            required_variables = ['name', 'image', 'imageproject', 'zone']
        else:
            print(f"Error: Invalid config_type '{config_type}'.")
            return False

        for variable in required_variables:
            if variable not in vm_details:
                print(f"Error: {variable} is missing in the {config_type} configuration.")
                return False
        return True
    
    def check_resource_group_exists(self, resource_group):
        try:
            result = subprocess.run(f"az group show --name {resource_group}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                return False
        except Exception as e:
            print("Error occurred while checking resource group existence:", e)
            return False
        
    def validate_password(password):
        if not (12 <= len(password) <= 123):
            return False
        
        character_types_count = sum([
            bool(re.search(r'[a-z]', password)),  
            bool(re.search(r'[A-Z]', password)),  
            bool(re.search(r'\d', password)),     
            bool(re.search(r'[!@#$%^&*()_+{}|:"<>?]', password))  
        ])
        
        if character_types_count < 3:
            return False
        
        return True

    def create_azure_vm(self, config):
        vm_details = {}
        start_parsing = False  
        for line in config.split("\n"):
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                start_parsing = True
                continue
            if start_parsing and "=" in line:
                key, value = line.split("=", 1)
                vm_details[key.strip()] = value.strip()

        if not self.validate_config(vm_details, "azure"):
            return

        name = vm_details.get('name')
        resource_group = vm_details.get('resource-group')
        image = vm_details.get('image')
        location = vm_details.get('location')
        admin_username = vm_details.get('admin-username')
        cpu = vm_details.get('cpu')
        disk_size = vm_details.get('disk-size')
        public_ip = vm_details.get('public-ip')
        password = vm_details.get('password')
        #ports = vm_details.get('ports')

        print("\nParsed Azure Config:")
        print("Name:", name)
        print("Resource Group:", resource_group)
        print("Image:", image)
        print("Location:", location)
        print("Admin Username:", admin_username)
        print("CPU:", cpu)
        print("Disk Size:", disk_size)
        print("Public IP:", public_ip)
        print("Password: ", password)
        #print("Ports:", ports)

        if not self.check_resource_group_exists(resource_group):
            print(f"The resource group '{resource_group}' does not exist.")
            print("Please create the resource group using the following command:")
            print(f"az group create --name {resource_group} --location {location}")
            return
        
        if password and "windows" in image.lower(): 
            if not self.validate_password(password):
                print("Error: The provided password does not meet complexity requirements.")
                print("Password must be between 12 and 123 characters in length and must contain at least 1 lower case character, 1 upper case character, 1 number, and 1 special character.")
                return

        azure_cli_command = f"az vm create --name {name} --resource-group {resource_group} --image {image} --location {location} --admin-username {admin_username}"

        if cpu:
            azure_cli_command += f" --size {cpu}"
        if disk_size:
            azure_cli_command += f" --os-disk-size-gb {disk_size}"
        if public_ip and public_ip.lower() == 'true':
            azure_cli_command += f" --public-ip-address {public_ip}" 
        if password and "windows" in image.lower():  
            azure_cli_command += f" --admin-password {password}"  
        #if ports:
         #   port_list = " ".join(ports.split(","))
          #  azure_cli_command += f" --ports {port_list}"

        print("\nAzure CLI Command:", azure_cli_command)
        while True:
            confirmation = input("Do you want to proceed with the creation of this VM? (yes/no): ").lower()
            if confirmation == "yes":
                try:
                    result = subprocess.run(azure_cli_command, shell=True, capture_output=True, text=True)
                    print("\nAzure CLI Result:", result.stdout)
                except subprocess.CalledProcessError as e:
                    print("Error occurred while creating Azure VM:", e)
                break  
            elif confirmation == "no":
                print("VM creation cancelled.")
                break 
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def create_gcp_vm(self, config):
        vm_details = {}
        start_parsing = False  
        for line in config.split("\n"):
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                start_parsing = True
                continue
            if start_parsing and "=" in line:
                key, value = line.split("=", 1)
                vm_details[key.strip()] = value.strip()

        if not self.validate_config(vm_details, "GCP"):
            return

        name = vm_details.get('name')
        project = vm_details.get('project')
        purpose = vm_details.get('purpose')
        os = vm_details.get('os')
        image = vm_details.get('image')
        imageproject = vm_details.get('imageproject')
        zone = vm_details.get('zone')
        machine_type = vm_details.get('machine-type')
        disk_size = vm_details.get('disk-size')
        public_ip = vm_details.get('public-ip')
        #ports = vm_details.get('ports')

        print("\nParsed GCP Config:")
        print("Name:", name)
        print("Project:", project)
        print("Purpose:", purpose)
        print("OS:", os)
        print("Image:", image)
        print("Image Project:", imageproject)
        print("Zone:", zone)
        print("Machine Type:", machine_type)
        print("Disk Size:", disk_size)
        print("Public IP:", public_ip)
        #print("Ports:", ports)

        gcp_cli_command = f"./google-cloud-sdk/bin/gcloud compute instances create {name} --project {project} --image {image} --image-project {imageproject} --zone {zone}"

        if purpose:
            metadata_str = f"purpose={purpose}"
        if os:
            metadata_str += f",os={os}"
            gcp_cli_command += f" --metadata {metadata_str}"
        if machine_type:
            gcp_cli_command += f" --machine-type {machine_type}"
        if disk_size:
            gcp_cli_command += f" --boot-disk-size {disk_size}"
        if public_ip and public_ip.lower() == 'true':
            gcp_cli_command += f" --address {public_ip}"
        #if ports:
         #   for port in ports.split(","):
          #      gcp_cli_command += f" --tags {port.strip()}"

        gcp_cli_command += " --format=json"

        print("\nGCP CLI Command:", gcp_cli_command)
        while True:
            confirmation = input("Do you want to proceed with the creation of this VM? (yes/no): ").lower()
            if confirmation == "yes":
                try:
                    result = subprocess.run(gcp_cli_command, shell=True, capture_output=True, text=True)
                    print("\nGCP CLI Result:", result.stdout)
                except subprocess.CalledProcessError as e:
                    print("Error occurred while creating GCP VM:", e)
                break  
            elif confirmation == "no":
                print("VM creation cancelled.")
                break 
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def parse_config(self, config):
        vm_details = {}
        start_parsing = False  
        for line in config.split("\n"):
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                start_parsing = True
                continue
            if start_parsing and "=" in line:
                key, value = line.split("=", 1)
                vm_details[key.strip()] = value.strip()
        return vm_details

    def write_vm_details(self, file, vm_details, platform):
        file.write(f"Platform: {platform}\n")
        file.write(f"Name: {vm_details.get('name')}\n")
        file.write(f"Project: {vm_details.get('project')}\n")
        file.write(f"Purpose: {vm_details.get('purpose')}\n")
        file.write(f"OS: {vm_details.get('os')}\n")
        file.write("\n")

    def generate_documentation(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"VMcreation_{timestamp}.txt"

        admin_name = os.getlogin()

        with open(filename, 'w') as file:
            file.write(f"Date Stamp: {timestamp}\n")
            file.write(f"System Admin Name: {admin_name}\n\n")

            if os.path.exists(self.azure_conf_file):
                with open(self.azure_conf_file, 'r') as azure_file:
                    azure_configs = azure_file.readlines()
                    for config in azure_configs:
                        vm_details = self.parse_config(config)
                        self.write_vm_details(file, vm_details, "Azure")

            if os.path.exists(self.gcp_conf_file):
                with open(self.gcp_conf_file, 'r') as gcp_file:
                    gcp_configs = gcp_file.readlines()
                    for config in gcp_configs:
                        vm_details = self.parse_config(config)
                        self.write_vm_details(file, vm_details, "GCP")

    def main(self):
        try:
            if os.path.exists(self.azure_conf_file):
                with open(self.azure_conf_file, 'r') as file:
                    azure_config = file.read()
                
                self.create_azure_vm(azure_config)

            if os.path.exists(self.gcp_conf_file):
                with open(self.gcp_conf_file, 'r') as file:
                    gcp_config = file.read()

                self.create_gcp_vm(gcp_config)
        except FileNotFoundError:
            print("Error: Configuration file not found. Please ensure that the configuration file exists before running the script.")
            return

        self.generate_documentation()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.rename(self.azure_conf_file, f"azure_{timestamp}.conf")
        os.rename(self.gcp_conf_file, f"gcp_{timestamp}.conf")

if __name__ == "__main__":
    vm_creation = VMCreation()
    vm_creation.main()
