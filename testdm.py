import instagrapi
import os
from dotenv import load_dotenv
import json

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

def load_users_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def send_dm(client, user_id, username, base_message):
    personalized_message = f"Hey {username},\n\n{base_message}"
    try:
        client.direct_send(personalized_message, [user_id])
        print(f"Sent message to {username}: {personalized_message}")
    except Exception as e:
        print(f"Error sending message to {username}: {str(e)}")


if __name__ == "__main__":
    load_dotenv()
    IG_USERNAME = os.getenv('IG_USERNAME')
    IG_PASSWORD = os.getenv('IG_PASSWORD')
    JSON_FILE_PATH = './data/reengoh2.json'  # Path to your JSON file
    IG_CREDENTIAL_PATH = './ig_settings.json'  # Path to your session file

    BASE_MESSAGE = 'Thank you for liking the post about Hydrafacial. We noticed you eyeing up something special, and guess what? We have an exclusive offer just for you!\n\nEnjoy Hydrafacial experience with code GLOW88. UP is $225; now at only $98. This limited-time treat (ends 12th Feb) lets you dive into a world where perfection is possible at a dazzling price.\n\nDon\'t wait - your VIP invitation expires soon! A surprise gift awaits you too. Book your appointment and unlock your inner radiance at Aura Aesthetics.\n\nCall or whatsapp 8838 8628 today!\n\nLove Aura \u2764\uFE0F'  # Replace with your message

    client = login_user(IG_USERNAME, IG_PASSWORD, IG_CREDENTIAL_PATH)
    client.delay_range = [30, 90]
    if client:
        users = load_users_from_json(JSON_FILE_PATH)
        for user in users:
            send_dm(client, user['id'], user['username'], BASE_MESSAGE)