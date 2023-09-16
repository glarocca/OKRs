# python-OKRs-statistics
This repository contains python clients to generate statistics about the total CPU/h and the number of users of the EGI Federated Infrastructure. 
Specifically, the statistics generated by these clients are:
- **Cloud CPU/h** consumed by the production VOs of EGI
- **HTC CPU/h** consumed by the production VOs of EGI
- Num. of **'active'**, **'total'** and **'actual' users** registered in the EGI Operations Portal. 

These statistics will be used by EGI to measure progress following the **Objectives and Key Results (OKRs)** goal-setting framework.

The statistics generated by these clients will be pushed in this Google <a href="https://docs.google.com/spreadsheets/d/1B1Sqf1UiN9pY_fGbWe5G1zKA2UzsekOVbLCtiiMFAXk/edit#">Worksheet</a> using the <a href="https://docs.gspread.org/en/v5.10.0/">gspread</a> API.

## Creating a Google Service Account
In order to read from and write data to Google Sheets in Python, we will have to create a **Google Service Account**.

_"A service account is a special kind of account used by an application or a virtual machine (VM) instance, not a person. 
Applications use service accounts to make authorized API calls, authorized as either the service account itself or as Google Workspace 
or Cloud Identity users through domain-wide delegation"._

**Instructions** to create a service account are the following:
* Head over to <a href="https://console.developers.google.com/">Google developer console</a> and click on “Create Project”.
* Fill in the required fields and click on “Create”. You will be redirected to the project home page once the project is created.
* Click on “Enable API and Services”.
* Search for Google Drive API and click on “Enable”. Do the same for the Google Sheets API.
* Click on “Create Credentials”
* Select “Google Drive API” as the API and “Web server” (e.g. Node.js, Tomcat, etc.) as where you will be calling the API from. Follow the image below to fill in the other options.
* Name the service account, then grant it a “Project” role with “Editor” access and click on “Continue”.
* The credentials will be created and downloaded as a JSON file. If everything is successful, you will see a screen similar to the image below.
* Copy the JSON file to your code directory and rename it to `credentials.json`
