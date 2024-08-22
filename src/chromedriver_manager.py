import subprocess, os, requests, zipfile, io

class ChromeVersionError(Exception):
    """
    Raised when the Chrome version cannot be determined.

    This exception is triggered when the Chrome version cannot be retrieved
    from the system's registry, either due to the registry key not existing
    or other issues during the query process.
    """
    pass

class ChromeDriverDownloadError(Exception):
    """
    Raised when the ChromeDriver download fails.

    This exception is raised when there is an issue with downloading the
    ChromeDriver binary, such as receiving a non-200 HTTP status code.
    """
    pass


class ChromeDriverManager:
    """
    A manager for handling ChromeDriver installation and version checking.

    This class provides methods to check the installed Chrome version, verify if
    the correct version of ChromeDriver is installed, download the correct version
    of ChromeDriver if necessary, and install it in a specified directory.
    """

    def __init__(self, chromedriver_dir: str = '.') -> None:
        """
        Initialize the ChromeDriverManager with the specified directory.

        Args:
            chromedriver_dir (str): The directory where the ChromeDriver binary
                                    is or will be located. Defaults to the current directory.
        """
        self.ENDPOINTS_JSON_CHROMEDRIVER_VERSIONS = fr'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
        self.URL_CHROMEDRIVER_LATEST_RELEASE_STABLE = fr'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE'

        self.chromedriver_dir = chromedriver_dir
        self.chromedriver_path = self.find_chromedriver(self.chromedriver_dir)
        self.chromedriver_version = self.get_chromedriver_version()
        self.chrome_version = self.get_chrome_version()
        self.update_status = self.update_checker()

    @staticmethod
    def get_chrome_version() -> str:
        """
        Get the installed version of Google Chrome.

        This method queries the Windows registry to find the installed version
        of Google Chrome.

        Returns:
            str: The installed version of Google Chrome.

        Raises:
            ChromeVersionError: If the Chrome version cannot be determined.
        """
        try:
            result = subprocess.run(
                ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                capture_output=True, text=True, check=True
            )
            output = result.stdout
            version_line = [line for line in output.splitlines() if 'version' in line.lower()]
            return version_line[0].split()[-1]

        except Exception as e:
            raise ChromeVersionError("Unable to determine Chrome version")

    def find_chromedriver(self, start_dir: str) -> str:
        """
        Search for the ChromeDriver binary in the specified directory.

        Args:
            start_dir (str): The directory where the search for ChromeDriver will start.

        Returns:
            str: The full path to the ChromeDriver binary if found, otherwise None.
        """
        for root, dirs, files in os.walk(start_dir):
            for file in files:
                if file == 'chromedriver.exe':
                    return os.path.join(root, file)
        return None

    def get_chromedriver_version(self) -> str:
        """
        Get the version of the installed ChromeDriver.

        This method checks the version of ChromeDriver by running the binary
        with the `--version` flag.

        Returns:
            str: The installed version of ChromeDriver if found, otherwise None.
        """
        if self.chromedriver_path:
            try:
                result = subprocess.run(
                    [self.chromedriver_path, '--version'],
                    capture_output=True, text=True, check=True
                )
                version = result.stdout.split()[1]
                return version
            
            except subprocess.CalledProcessError:
                return None
            
        else:
            return None

    def update_checker(self) -> bool:
        """
        Check if the ChromeDriver version matches the Chrome version.

        Returns:
            bool: True if the ChromeDriver version matches the Chrome version, False otherwise.
        """
        return self.chrome_version == self.chromedriver_version if self.chrome_version else None

    def get_link_version(self, link: str) -> str:
        """
        Get the download link for the correct version of ChromeDriver.

        Args:
            link (str): The URL to the JSON file containing ChromeDriver versions and download links.

        Returns:
            str: The download URL for the correct version of ChromeDriver, or None if not found.
        """
        response = requests.get(link)

        if response.status_code == 200:
            data = response.json()

            for channel_info in data['channels'].values():
                if channel_info['version'] == self.chrome_version:
                    for item in channel_info['downloads']['chromedriver']:
                        if item['platform'] == 'win64':
                            return item['url']
            return None

    def download_chromedriver(self, link: str, _dir: str) -> None:
        """
        Download and extract the ChromeDriver binary to the specified directory.

        Args:
            link (str): The URL to download ChromeDriver.
            _dir (str): The directory to save and extract the ChromeDriver binary.

        Raises:
            ChromeDriverDownloadError: If the download fails.
        """
        os.makedirs(_dir, exist_ok=True)
        response = requests.get(link)
        
        if response.status_code != 200:
            raise ChromeDriverDownloadError(f"Failed to download ChromeDriver: HTTP {response.status_code}")

        file_like_object = io.BytesIO(response.content)
        is_zip = zipfile.is_zipfile(file_like_object)

        if is_zip:
            with zipfile.ZipFile(file_like_object) as z:
                z.extractall(_dir)
        else:
            file_name = os.path.join(_dir, os.path.basename(link))
            with open(file_name, 'wb') as file:
                file.write(response.content)

    def install(self) -> str:
        """
        Ensure the correct version of ChromeDriver is installed.

        This method checks if the installed ChromeDriver matches the version of Chrome.
        If not, it downloads and installs the correct version.

        Returns:
            str: The path to the installed ChromeDriver.
        """
        if self.chrome_version == self.chromedriver_version:
            return self.chromedriver_path
        else:
            link = self.get_link_version(self.ENDPOINTS_JSON_CHROMEDRIVER_VERSIONS)

            if link is None:
                self.chrome_version = requests.get(self.URL_CHROMEDRIVER_LATEST_RELEASE_STABLE).text
                link = self.get_link_version(self.ENDPOINTS_JSON_CHROMEDRIVER_VERSIONS)

            self.download_chromedriver(link, self.chromedriver_dir)
            self.chromedriver_path = self.find_chromedriver(self.chromedriver_dir)
            return self.chromedriver_path
        