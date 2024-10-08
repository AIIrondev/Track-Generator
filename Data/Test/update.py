import os
import sys
import requests
import zipfile
import shutil
import json

with open('Data/config/trackgenerator.config.json') as f:
    config = json.load(f)
LOCAL_VERSION_FILE = config['version']
print(LOCAL_VERSION_FILE)
UPDATE_FOLDER = 'update_files/'
API_URL = 'https://api.github.com/repos/AIIrondev/Track-Generator/releases/latest'
DOWNLOAD_PATH = 'Trackgenerator.zip'
class Update:
    def get_local_version():
        try:
            return LOCAL_VERSION_FILE
        except FileNotFoundError:
            return "0.0.0"

    def get_latest_release():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.content}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None

    def check_for_update():
        local_version = get_local_version()
        latest_release = get_latest_release()

        if latest_release:
            latest_version = latest_release['tag_name']
            print(f"Local version: {local_version}, Latest version: {latest_version}")

            if latest_version > local_version:
                print(f"New version available: {latest_version}")
                return latest_release
            else:
                print("You are already on the latest version.")
                return None
        else:
            print("No update information found.")
            return None

    def download_update(asset_url):
        print(f"Downloading update from: {asset_url}")
        response = requests.get(asset_url, stream=True)

        if response.status_code == 200:
            print("Update is getting downloaded...")
            with open(DOWNLOAD_PATH, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print("Update downloaded.")
            return True
        else:
            print(f"Failed to download update: {response.status_code}")
            return False

    def apply_update():
        print("Applying update...")
        try:
            with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
                zip_ref.extractall(UPDATE_FOLDER)
            for root, dirs, files in os.walk(UPDATE_FOLDER):
                for file in files:
                    full_path = os.path.join(root, file)
                    target_path = os.path.join(os.getcwd(), file)
                    shutil.move(full_path, target_path)
            print("Update applied successfully.")
            os.remove(DOWNLOAD_PATH)
            shutil.rmtree(UPDATE_FOLDER)
            return True
        except Exception as e:
            print(f"Failed to apply update: {e}")
            return False

    def restart_application():
        print("Restarting application...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def main():
        latest_release = check_for_update()

        if latest_release:
            for asset in latest_release['assets']:
                if asset['name'] == 'Trackgenerator.zip':
                    asset_url = asset['browser_download_url']
                    if download_update(asset_url):
                        if apply_update():
                            print("Update complete. Restarting now...")
                            restart_application()
                    break
            else:
                print("Update.zip file not found in the release assets.")
        else:
            print("No updates to apply.")

    if __name__ == "__main__":
        main()
