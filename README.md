# ChromeDriverManager

**Chromedriver Manager** is a Python library that automates the download and installation of the latest version of Chromedriver, making it easier to set up environments for Robotic Process Automation (RPA) applications. Ideal for developers using Selenium or other tools that require Chromedriver, this package ensures that you always have the correct version, eliminating compatibility issues between the browser and the driver.

### Current version: 1.0.0

### Features

* **Automatic Download:** Automatically downloads and installs the appropriate version of ChromeDriver based on the installed version of Chrome.
* **Compatibility Assurance:** Ensures that the ChromeDriver version matches the installed Chrome version, avoiding version mismatches.
* **Easy Integration:** Seamlessly integrates into existing automation scripts, reducing setup and configuration time.
* **Customization:** Offers flexibility to customize the download directory and other aspects of the ChromeDriver installation process.

### Note

* **Current Support:** The current version of `ChromeDriverManager` supports only Windows 64-bit systems. Support for other platforms will be added in future releases.

### Usage Example


```
from chromedriver_manager import ChromeDriverManager

# Instantiate the ChromeDriver manager
manager = ChromeDriverManager()

# Check and install the correct ChromeDriver version if needed
chromedriver_path = manager.install()

print(f"ChromeDriver is installed at: {chromedriver_path}")

```

### Usage Example with Selenium

Here is how you can use `ChromeDriverManager` with Selenium to automate browser tasks:

```
from selenium import webdriver
from chromedriver_manager import ChromeDriverManager

# Instantiate the ChromeDriver manager
manager = ChromeDriverManager()

# Ensure the correct version of ChromeDriver is installed and get its path
chromedriver_path = manager.install()

# Set up the WebDriver with the path to the ChromeDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Open a website and perform actions
driver.get('https://www.example.com')

# Print the title of the webpage
print(f"Page title is: {driver.title}")

# Close the browser
driver.quit()

```

### Usage Example with Selenium and Service

Here is how you can use `ChromeDriverManager` with Selenium’s `Service` to automate browser tasks:

```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_manager import ChromeDriverManager

# Instantiate the ChromeDriver manager
manager = ChromeDriverManager()

# Ensure the correct version of ChromeDriver is installed and get its path
chromedriver_path = manager.install()

# Set up the WebDriver with the path to the ChromeDriver using Service
service = Service(executable_path=chromedriver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open a website and perform actions
driver.get('https://www.example.com')

# Print the title of the webpage
print(f"Page title is: {driver.title}")

# Close the browser
driver.quit()

```

### Exceptions

The library raises custom exceptions to handle specific errors:

* `ChromeVersionError`: Raised when the Chrome version cannot be determined.
* `ChromeDriverDownloadError`: Raised when the ChromeDriver download fails.

### Support

For support, please contact:

Fernando Manfré: fn.manfre@gmail.com

### Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.
