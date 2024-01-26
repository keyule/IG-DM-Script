import json
import os

def load_data_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return []

def compare_data(file1, file2, folder='data'):
    file_path1 = os.path.join(folder, file1)
    file_path2 = os.path.join(folder, file2)

    data1 = load_data_from_json(file_path1)
    data2 = load_data_from_json(file_path2)

    if data1 == data2:
        print("The data sets are identical.")
        return

    set1 = {d['username'] for d in data1}
    set2 = {d['username'] for d in data2}

    new_users = set2 - set1
    removed_users = set1 - set2

    if new_users:
        print("New users:")
        for i, user in enumerate(new_users, 1):
            print(f"{i}. {user}")
    else:
        print("No new users.")

    if removed_users:
        print("\nUsers no longer present:")
        for i, user in enumerate(removed_users, 1):
            print(f"{i}. {user}")
    else:
        print("No users removed.")

    if not new_users and not removed_users:
        print("No differences found in users.")

if __name__ == "__main__":
    filename1 = 'likers_data_20240118_154121.json'
    filename2 = 'likers_data_20240119_090952.json'
    compare_data(filename1, filename2)