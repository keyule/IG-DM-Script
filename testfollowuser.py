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

def follow_user(client, username_to_follow):
    try:
        user_id = client.user_id_from_username(username_to_follow)
        client.user_follow(user_id)
        print(f"Followed the user: {username_to_follow}")
    except Exception as e:
        print(f"Error following the user {username_to_follow}: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    IG_USERNAME = os.getenv('IG_USERNAME')
    IG_PASSWORD = os.getenv('IG_PASSWORD')
    TARGET_USERNAME = 'fxi.09'  # Replace with the username of the person you want to follow
    IG_CREDENTIAL_PATH = './ig_settings.json'  # Path to your session file

    client = login_user(IG_USERNAME, IG_PASSWORD, IG_CREDENTIAL_PATH)
    if client:
        follow_user(client, TARGET_USERNAME)
