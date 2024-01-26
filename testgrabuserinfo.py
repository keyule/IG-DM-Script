import instagrapi
import os
from dotenv import load_dotenv

def login_user(username, password, session_file):
    try:
        client = instagrapi.Client()
        
        # Check if the session file exists before trying to load it
        if session_file and os.path.exists(session_file):
            client.load_settings(session_file)
            print("Loaded session data from file.")
        else:
            # If no session data is found, perform a fresh login
            client.login(username, password)
            print(f"Logged in as {username}")

            # Save the session data to the JSON file for future use
            if session_file:
                client.dump_settings(session_file)
                print("Session data saved to file.")

        return client
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return None

def get_user_info(client, user_id):
    try:
        user_info = client.user_info(user_id)
        print(user_info)
        print(f"Username: {user_info.username}")
        print(f"Full Name: {user_info.full_name}")
        print(f"Is Private: {user_info.is_private}")
        print(f"Is Verified: {user_info.is_verified}")
        # Add more fields as needed
    except Exception as e:
        print(f"Error retrieving user info: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    IG_USERNAME = os.getenv('IG_USERNAME')
    IG_PASSWORD = os.getenv('IG_PASSWORD')
    session_file = './ig_settings.json'  # Path to your session file
    user_id = 46019678526  # Replace with the target user ID

    client = login_user(IG_USERNAME, IG_PASSWORD, session_file)
    if client:
        get_user_info(client, user_id)