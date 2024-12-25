'''
FILE: src/notion/database.py
DESCRIPTION: This file contains utility functions for interacting with Notion databases.
'''

# global imports
import json
import requests
import os

def get_rows(database_id, headers, filter_obj=None, sorts=None, page_size=100, start_cursor=None) -> list:
    """
    Retrieves (queries) all rows (pages) from the given Notion database.

    :param database_id: The ID of the Notion database.
    :param headers: Headers including authorization for the Notion API.
    :param filter_obj: (Optional) A filter object to narrow down the query results.
                      See the Notion API docs for the structure.
    :param sorts: (Optional) A list of sort instructions for the query.
                  E.g. [{ "timestamp": "created_time", "direction": "descending" }]
    :param page_size: (Optional) Number of pages per request. Max 100.
    :param start_cursor: (Optional) Used for pagination. If provided, starts from this cursor.
    :return: A list of page objects that belong to this database (possibly multiple requests if needed).

    sample usage:
        rows = get_rows(DATABASE_ID, HEADERS)
    """

    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    all_pages = []
    has_more = True
    current_cursor = start_cursor

    while has_more:
        payload = {
            "page_size": page_size,
        }
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        if current_cursor:
            payload["start_cursor"] = current_cursor

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            print(f"Failed to query database: {response.status_code}")
            print(response.text)
            return []

        data = response.json()
        all_pages.extend(data.get("results", []))

        # Check for pagination
        has_more = data.get("has_more", False)
        current_cursor = data.get("next_cursor", None)

    return all_pages


def get_row(page_id, headers) -> dict:
    """
    Retrieves a specific page (row) from Notion by its page ID.

    :param page_id: The ID of the page (row) in Notion.
    :param headers: Headers including authorization for the Notion API.
    :return: The JSON data for the page, or None if an error occurred.

    sample usage:
        row = get_row(row_id, HEADERS)
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        print(response.text)
        return None


def add_row(database_id, headers, properties):
    """
    Creates a new page (row) in the specified Notion database.

    :param database_id: The ID of the Notion database.
    :param headers: Headers including authorization for the Notion API.
    :param properties: A dictionary specifying the properties of the row.
                       The keys should match the database property names or IDs.
                       The values should be property values conforming to the Notion schema.
    :return: The newly created page object as a dict, or None if an error occurred.

    sample usage:
        properties = {
            "Name": {"title": [{"text": {"content": "New Job Application"}}]},
        }
        new_row = add_row(DATABASE_ID, HEADERS, properties)
    """
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Row added successfully!")
        return response.json()
    else:
        print(f"Failed to add row: {response.status_code}")
        print(response.text)
        return None


def update_row(page_id, headers, properties):
    """
    Updates an existing page (row) in Notion with new property values.

    :param page_id: The ID of the page to update.
    :param headers: Headers including authorization for the Notion API.
    :param properties: A dictionary specifying the updated property values, 
                       matching the Notion database schema.
    :return: The updated page object as a dict, or None if an error occurred.

    sample usage:
        properties = {
            "Name": {"title": [{"text": {"content": "Updated Job Application"}}]},
        }
        updated_row = update_row(row_id, HEADERS, properties)
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": properties
    }

    # Notion requires a PATCH request for updates
    response = requests.patch(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Row updated successfully!")
        return response.json()
    else:
        print(f"Failed to update row: {response.status_code}")
        print(response.text)
        return None


def delete_row(page_id, headers):
    """
    Archives (effectively "deletes") a page (row) in Notion.
    Notion doesn't have a true 'delete' via the API, 
    so we set `archived` to True to remove it from the workspace.

    :param page_id: The ID of the page (row) to archive.
    :param headers: Headers including authorization for the Notion API.
    :return: True if successful, False otherwise.

    sample usage:
        delete_row(row_id, HEADERS)
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "archived": True
    }

    response = requests.patch(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Row archived (deleted) successfully!")
        return True
    else:
        print(f"Failed to archive row: {response.status_code}")
        print(response.text)
        return False


def get_db_schema(database_id, headers, output_path="data/notion_db_schema.json"):
    """
    Retrieves the schema of the specified Notion database and saves it to a JSON file.

    :param database_id: The ID of the Notion database.
    :param headers: Headers including authorization for the Notion API.
    :param output_path: The file path where the schema will be saved.
    :return: The database schema as a dictionary, or None if an error occurred.

    sample usage:
        schema = get_db_schema(DATABASE_ID, HEADERS)
    """
    url = f"https://api.notion.com/v1/databases/{database_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        schema = response.json()
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2)
        print(f"Database schema saved to {output_path}")
        return schema
    else:
        print(f"Failed to retrieve database schema: {response.status_code}")
        print(response.text)
        return None


def update_db_schema(database_id, headers, updates):
    """
    Updates the schema of the specified Notion database.

    :param database_id: The ID of the Notion database.
    :param headers: Headers including authorization for the Notion API.
    :param updates: A dictionary containing the updates to be made.
    
    Example structure:
        {
            "properties": {
                "New Property Name": {
                    "type": "select",
                    "select": {
                        "options": [
                            {"name": "New Option", "color": "blue"}
                        ]
                    }
                },
                "Existing Property Name": {
                    "type": "multi_select",
                    "multi_select": {
                        "options": [
                            {"name": "Another Option", "color": "green"}
                        ]
                    }
                },
                "Rename Property": {
                    "new_name": "Renamed Property"
                }
            }
        }
    :return: The updated database object as a dictionary, or None if an error occurred.

    sample usage:
        updates = {
            "properties": {...}
        }
        updated_db = update_db_schema(DATABASE_ID, HEADERS, updates)
    """
    url = f"https://api.notion.com/v1/databases/{database_id}"

    # Fetch current schema
    current_schema = get_db_schema(database_id, headers)
    if not current_schema:
        print("Cannot update schema without fetching the current schema.")
        return None

    # Prepare the properties to update
    updated_properties = {}
    for prop_name, prop_changes in updates.get("properties", {}).items():
        if "new_name" in prop_changes:
            # Rename the property
            updated_properties[prop_changes["new_name"]] = current_schema["properties"].get(prop_name)
            del updated_properties[prop_changes["new_name"]]["name"]  # Remove old name
            updated_properties[prop_changes["new_name"]]["name"] = prop_changes["new_name"]
        else:
            # Update or add options for select/multi_select
            if prop_changes["type"] in ["select", "multi_select"]:
                property_obj = current_schema["properties"].get(prop_name)
                if not property_obj:
                    print(f"Property '{prop_name}' does not exist in the database.")
                    continue

                # Merge existing options with new ones
                existing_options = property_obj.get(prop_changes["type"], {}).get("options", [])
                new_options = prop_changes[prop_changes["type"]].get("options", [])
                # Avoid duplicates based on option name
                existing_option_names = {opt["name"] for opt in existing_options}
                for opt in new_options:
                    if opt["name"] not in existing_option_names:
                        existing_options.append(opt)
                # Prepare the updated property
                updated_properties[prop_name] = {
                    "type": prop_changes["type"],
                    prop_changes["type"]: {
                        "options": existing_options
                    }
                }
            else:
                print(f"Property type '{prop_changes['type']}' not supported for updates.")
                continue

    if not updated_properties:
        print("No valid updates found to apply.")
        return None

    payload = {
        "properties": updated_properties
    }

    response = requests.patch(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        updated_database = response.json()
        print("Database schema updated successfully!")
        # Optionally, save the updated schema
        get_db_schema(database_id, headers)  # This will overwrite the existing schema file
        return updated_database
    else:
        print(f"Failed to update database schema: {response.status_code}")
        print(response.text)
        return None
