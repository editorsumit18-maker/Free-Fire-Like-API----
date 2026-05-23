import requests
import json

UIDPASS_FILE = "uidpass.json"
TOKEN_FILE = "tokens.json"
API_URL = ""

def read_uidpass():
    try:
        with open(UIDPASS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print("UIDPASS LOADED:", data)
            return data
    except Exception as e:
        print("Error reading uidpass.json:", e)
        return []

def fetch_token(uid, password):
    url = f"{API_URL}?uid={uid}&password={password}"
    print("Request URL:", url)

    try:
        response = requests.get(url, timeout=10)
        print("Status Code:", response.status_code)

        response.raise_for_status()
        data = response.json()
        print("API Response:", data)

        # ✅ handle both token types
        return data.get("token") or data.get("access_token")

    except Exception as e:
        print(f"Error fetching token for UID {uid}:", e)
        return None

def update_token_file(token_list):
    try:
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            json.dump(token_list, f, ensure_ascii=False, indent=4)
        print("tokens.json written successfully ✅")
    except Exception as e:
        print("Error writing tokens.json:", e)

def main():
    print("=== SCRIPT STARTED ===")

    uidpass_list = read_uidpass()

    if not uidpass_list:
        print("No UIDPASS data found ❌")
        return

    new_tokens = []

    for item in uidpass_list:
        print("Processing:", item)

        uid = item.get("uid")
        password = item.get("password")

        if not uid or not password:
            print("Invalid UID/PASSWORD format ❌")
            continue

        token = fetch_token(uid, password)

        if token:
            print("Token received ✅")
            new_tokens.append(token)   # 🔥 FIXED LINE
        else:
            print("No token received ❌")

    if new_tokens:
        update_token_file(new_tokens)
        print("tokens.json updated successfully ✅")
    else:
        print("No tokens updated ❌")

if __name__ == "__main__":
    main()
