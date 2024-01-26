import instagrapi
import os
import time
import json
from datetime import datetime
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

def find_user_id_by_username(client, target_username):
    try:
        user_id = client.user_id_from_username(target_username)
        print(f"User ID of {target_username}: {user_id}")
        return user_id
    except Exception as e:
        print(f"Failed to retrieve user ID: {str(e)}")

def get_latest_posts(client, user_id, max_posts=15):
    try:
        posts = client.user_medias_gql(user_id, amount=max_posts)
        post_list = [{
            "id": post.pk,
            "caption": post.caption_text,
            "taken_at": post.taken_at,
            "like_count": post.like_count
        } for post in posts]

        for i, post in enumerate(post_list):
            print(f"{i+1}: ID = {post['id']}, Caption = {post['caption'][:30]}..., Taken At: {post['taken_at']}, Likes: {post['like_count']}")

        return post_list
    except Exception as e:
        print(f"Error fetching posts: {str(e)}")
        return []

def get_post_likes(client, post_id):
    likers_data = []
    try:
        likes = client.media_likers(post_id)
        for index, liker in enumerate(likes, start=1):
            print(f"{index}. ID: {liker.pk}, Username: {liker.username}")
            likers_data.append({'id': liker.pk, 'username': liker.username})
    except Exception as e:
        print(f"Error retrieving post likes: {str(e)}")
    return likers_data

def save_data_to_json(data, base_filename, folder='data'):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{folder}/{base_filename}_{timestamp}.json"
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    load_dotenv()
    IG_USERNAME = os.getenv('IG_USERNAME')
    IG_PASSWORD = os.getenv('IG_PASSWORD')
    TARGET_USERNAME = os.getenv('TARGET_USERNAME')

    IG_CREDENTIAL_PATH = './ig_settings.json'

    client = login_user(IG_USERNAME, IG_PASSWORD, IG_CREDENTIAL_PATH)
    client.delay_range = [1, 3]
    if client:
        user_id = find_user_id_by_username(client, TARGET_USERNAME)

    print("\nFetching latest posts...")
    posts = get_latest_posts(client, user_id)

    # Choose a post
    post_index = int(input("Enter the number of the post to see likes: ")) - 1
    selected_post_id = posts[post_index]['id']

    # Get likes for the selected post
    print(f"\nUsers who liked post ID {selected_post_id}:")
    likers = get_post_likes(client, selected_post_id)
    save_data_to_json(likers, 'likers_data')


