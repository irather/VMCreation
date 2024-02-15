# VMCreation

This is a Python script that will automate the creation and deployment of Virtual Machines on Azure and GCP using the CLI’s for each platform.

## Prerequisites

- Python 3.11.6 installed
- Azure CLI and GCP CLI installed
- azure.conf and GCP.conf is created and is located in root directory of this project

## Setup

1. (Optional) Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - On Unix or MacOS:

     ```bash
     source venv/bin/activate
     ```

3. Install Azure CLI and GCP CLI for your specific machine:

4. Run the automate.py file:

   ```bash
   python3 automate.py
   ```

5. (Optional) Deactivate the virtual environment:

   ```bash
   deactivate
   ```

## Usage

- Once your configs have been created, run the automate.py file and follow the steps after running the file. If no output is given
  for the results of the VM creation and no error is thrown for the config being wrong, copy the given command and run it locally to
  view the issue.

## Notes

- The additional VM configurations I added for the Azure config are _cpu_, _disk-size_, and _public-ip_ and for the GCP config they
  are _machine-type_, _disk-size_, and _public-ip_
- Make sure your Azure CLI and GCP CLI is properly installed and configured with the necessary permissions.
  - for the GCP CLI, please ensure that the google-cloud-sdk folder that is created after installing GCP CLI is location in the root
    folder of this project
- If using a virtual environment, activate it before running the shell.
- Make sure an azure.conf and GCP.conf file is created and stored in the root directory of the project and is correctly configured for
  the specific VM that is being created
  - When creating a Windows VM in Azure, please specify a password in the azure.conf file
