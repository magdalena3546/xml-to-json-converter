import xml.etree.ElementTree as ET
import json


# create exception for duplication
class DuplicateEmployee(Exception):
    def __init__(self, email):
        super().__init__(f"Duplicate employee: {email}")

# parse xml file to elementree
async def parse_xml(file):
    content = await file.read()
    root = ET.fromstring(content)
    return root
# Create dictionary for group managers and their employees, choose top managers (without manager)
# Create set for unique emails to avoid duplicate employees
def return_managers(root):
    managers = {}
    top_managers_list = []
    unique_emails = set()
    for employee in root:
        employee_email = employee.find('./field[@id="email"]').text
        employee_manager = employee.find('./field[@id="manager"]').text
        if employee_email in unique_emails:
            raise DuplicateEmployee(employee_email)
        else:
            unique_emails.add(employee_email)
        if employee_manager is None:
            top_managers_list.append(employee_email)
        elif employee_manager not in managers:
            managers[employee_manager] = []
            managers[employee_manager].append(employee_email)
        else:
            managers[employee_manager].append(employee_email)
    return managers, top_managers_list

# Function to create hierarchy for json file
def create_hierarchy(manager, root):
    employee_data ={}
    managers, _ = return_managers(root)
    data = {"employee":employee_data}
    employee_data["email"] = manager
    employee_data["direct_reports"] = []
    if manager in managers:
        for report in managers[manager]:
            employee_data["direct_reports"].append(create_hierarchy(report, root))
    return data

# Create data for json file by iterate through top managers list
def create_json(root):
    data_for_json = []
    _, top_managers_list = return_managers(root)
    for manager in top_managers_list:
        data_for_json.append(create_hierarchy(manager, root))
    
    # Create json file and write data
    with open("output.json", "w") as file:
        json.dump(data_for_json, file, indent=2)
    
    