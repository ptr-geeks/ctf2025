import requests
import yaml
import argparse

def get_challenges(url, token):
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{url}/api/v1/challenges", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching challenges: {response.status_code} - {response.text}")

def get_challenge(url, token, challenge_id):
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{url}/api/v1/challenges/{challenge_id}", headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        raise Exception(f"Error fetching challenge {challenge_id}: {response.status_code} - {response.text}")


def post_challenge(url, token, challenge_data, flag_data, files):
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(f"{url}/api/v1/challenges", headers=headers, json=challenge_data)
    if response.status_code != 200:
        raise Exception(f"Error creating challenge: {response.status_code} - {response.text}")

    challenge = response.json()
    flag_data["challenge"] = challenge["data"]["id"]

    response = requests.post(f"{url}/api/v1/flags", headers=headers, json=flag_data)
    if response.status_code != 200:
        raise Exception(f"Error creating flag: {response.status_code} - {response.text}")

    files_data = [("file", open(file, "rb")) for file in files]
    values = {
        "challenge": challenge["data"]["id"],
        "type": "challenge",
    }
    del headers["Content-Type"]
    response = requests.post(f"{url}/api/v1/files", headers=headers, files=files_data, data=values)
    if response.status_code != 200:
        raise Exception(f"Error uploading files: {response.status_code} - {response.text}")

def put_challenge(url, token, challenge_id, challenge_data):
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    response = requests.put(f"{url}/api/v1/challenges/{challenge_id}", headers=headers, json=challenge_data)
    if response.status_code != 200:
        raise Exception(f"Error updating challenge: {response.status_code} - {response.text}")

def prepare_challenge_standard(challenge):
    chall_data = {
        "name": challenge["name"],
        "category": challenge["category"],
        "description": challenge["description"],
        "value": challenge["value"],
        "state": challenge["state"],
        "type": challenge["type"],
    }
    if "connection_info" in challenge:
        chall_data["connection_info"] = challenge["connection_info"]
    flag_data = {
        "content": challenge["flag"],
        "data": "",
        "type": "standard",
        "challenge": 0 # Placeholder
    }
    files = challenge.get("files", [])
    return chall_data, flag_data, files

def prepare_challenge_instanced(challenge):
    chall_data = {
        "name": challenge["name"],
        "category": challenge["category"],
        "description": challenge["description"],
        "value": challenge["value"],
        "state": challenge["state"],
        "type": challenge["type"],
        "connection_info": challenge.get("connection_info", "Use the instancer on the top left corner"),
        "flag_base": challenge["flag"],
        "flag_type": challenge["instanced"]["flag_type"],
        "challenge_type": challenge["instanced"]["challenge_type"],
        "duration": challenge["instanced"]["duration"],
        "cooldown": challenge["instanced"]["cooldown"],
        "repository": challenge["instanced"]["repository"],
        "chart": challenge["instanced"]["chart"],
        "chart_version": challenge["instanced"]["chart_version"],
        "values": challenge["instanced"]["values"].strip(),
    }
    flag_data = {
        "content": "",
        "data": "",
        "type": "instanced",
        "challenge": 0 # Placeholder
    }
    files = challenge.get("files", [])
    return chall_data, flag_data, files

def main():
    parser = argparse.ArgumentParser(description="CTFd API Client")
    parser.add_argument("--url", required=True, help="Base URL of the CTFd instance")
    parser.add_argument("--token", required=True, help="API token for authentication")
    parser.add_argument("--config", required=False, help="Path to configuration file", default="challs.yml")
    args = parser.parse_args()

    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    challenges = get_challenges(args.url, args.token)
    challenges = {c["name"]: c for c in challenges["data"]} 

    for challenge in config["challenges"]:
        print(f"> Processing challenge: {challenge['name']}")

        if challenge["name"] in challenges:
            print(">> Challenge already exists, skipping.")
            continue

        if challenge["type"] == "standard":
            challenge_data, flag_data, files = prepare_challenge_standard(challenge)
        elif challenge["type"] == "instanced":
            challenge_data, flag_data, files = prepare_challenge_instanced(challenge)
        else:
            print(f">> Unknown challenge type {challenge['type']} for challenge {challenge['name']}, skipping.")
            continue
        
        post_challenge(args.url, args.token, challenge_data, flag_data, files)
        print(f">> Challenge {challenge['name']} created successfully.")


if __name__ == "__main__":
    main()
