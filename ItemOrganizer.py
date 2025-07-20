#!/usr/bin/env python3
import json
import os
import sys

# Filenames
DATA_FILE = 'storage.json'
SCHEMA_FILE = 'storage_schema.json'

# Load existing data or initialize
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"items": []}

# Save current data to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Basic integrity check against schema
def validate_data(data):
    try:
        schema = json.load(open(SCHEMA_FILE))
    except Exception as e:
        print(f"ERROR: Cannot load schema: {e}")
        return False
    # Top-level must have 'items' list
    if 'items' not in data or not isinstance(data['items'], list):
        print("ERROR: Data must contain 'items' as a list.")
        return False
    # Determine required fields
    required = schema.get('required') or list(schema.get('properties', {}).keys())
    props = schema.get('properties', {})
    type_map = {
        'string': str,
        'integer': int,
        'number': (int, float)
    }
    # Check each item
    for idx, item in enumerate(data['items'], 1):
        if not isinstance(item, dict):
            print(f"ERROR: Item #{idx} is not an object.")
            return False
        for field in required:
            if field not in item:
                print(f"ERROR: Item #{idx} missing field '{field}'.")
                return False
            expected = props.get(field, {}).get('type')
            if expected:
                pytype = type_map.get(expected)
                if not isinstance(item[field], pytype):
                    print(f"ERROR: Field '{field}' in item #{idx} must be of type {expected}.")
                    return False
    return True

# Add a new item
def add_item(data):
    item = {}
    item['category'] = input("Item Category: ")
    item['subcategory'] = input("Item Subcategory: ")
    item['brand'] = input("Item Brand: ")
    item['model_number'] = input("Item Model Number: ")
    item['quantity'] = int(input("Item Quantity: "))
    item['price_per_piece'] = float(input("Item Price per piece: "))
    item['storage_description'] = input("Item Storage Description: ")
    item['notes'] = input("Item Notes: ")
    data['items'].append(item)
    save_data(data)
    print("\nItem added.\n")

# Find an existing item
def find_item(data):
    key = input("What Item are you looking for (Modelnumber): ")
    for item in data['items']:
        if item['model_number'] == key:
            print(f"\nStorage Description: {item['storage_description']}")
            print(f"Notes: {item['notes']}\n")
            return
    print("\nItem not found.\n")

# Change a field of an existing item
def change_item(data):
    key = input("What Item do you want to change? (Modelnumber): ")
    for item in data['items']:
        if item['model_number'] == key:
            print("\nWhat do you want to change?")
            choices = {
                '1': 'category',
                '2': 'subcategory',
                '3': 'brand',
                '4': 'model_number',
                '5': 'quantity',
                '6': 'price_per_piece',
                '7': 'storage_description',
                '8': 'notes'
            }
            print("1 Category\n2 Subcategory\n3 Brand\n4 Model Number\n5 Quantity\n6 Price\n7 Storage\n8 Notes")
            choice = input("Choose field number: ")
            field = choices.get(choice)
            if not field:
                print("\nInvalid choice.\n")
                return
            new = input(f"Enter new value for {field}: ")
            # Cast types for numeric fields
            if field == 'quantity':
                item[field] = int(new)
            elif field == 'price_per_piece':
                item[field] = float(new)
            else:
                item[field] = new
            save_data(data)
            print("\nItem updated.\n")
            return
    print("\nItem not found.\n")

# Delete an existing item
def delete_item(data):
    key = input("What Item do you want to delete? (Modelnumber | abort): ")
    if key.lower() == 'abort':
        print("\nAbort. Returning to main menu.\n")
        return
    for idx, item in enumerate(data['items']):
        if item['model_number'] == key:
            confirm = input(f"You want to delete - {key} in {item['storage_description']} - are you sure? (y/n): ")
            if confirm.lower() == 'y':
                data['items'].pop(idx)
                save_data(data)
                print(f"\nSuccessfully deleted the Item {key}\n")
            else:
                print("\nDeletion cancelled.\n")
            return
    print("\nItem not found.\n")

# Main loop
def main():
    data = load_data()
    print("Welcome to your storage system\n")
    while True:
        cmd = input("What do you want to do? (addItem | findItem | changeItem | deleteItem | exit): ")
        if cmd == 'addItem':
            add_item(data)
        elif cmd == 'findItem':
            find_item(data)
        elif cmd == 'changeItem':
            change_item(data)
        elif cmd == 'deleteItem':
            delete_item(data)
        elif cmd == 'exit':
            save_data(data)
            if validate_data(data):
                print("Data integrity check passed. Exiting.\n")
                sys.exit(0)
            else:
                print("Data integrity check failed. Please correct your data and try again.\n")
        else:
            print("\nInvalid command.\n")

if __name__ == '__main__':
    main()
