import platform
import requests


class GetChromeVersionForCurrentOS:

    def __init__(self):
        self.user_os = platform.system()
        self.chrome_api_endpoint = "https://versionhistory.googleapis.com/v1/chrome/platforms/linux/channels/stable/versions/all/releases?filter=endtime=none"
        self.current_chrome_version = None

    def get_chrome_version(self):
        request_chrome_version_for_current_os = requests.get(self.chrome_api_endpoint)
        self.current_chrome_version = request_chrome_version_for_current_os.json()['releases'][0]['version']
        return self.current_chrome_version
