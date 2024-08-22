# Fast ChromeDriver Manager

**Fast Chromedriver Manager** is a Python library that automates the download and installation of the correct version of Chromedriver for your browser, ensuring seamless compatibility. This makes it easier to set up environments for Robotic Process Automation (RPA) applications. Ideal for developers using Selenium or other tools that require Chromedriver, this package guarantees that you always have the right version, eliminating compatibility issues between the browser and the driver.

### Current version: 1.0.1

### Features

* **Automatic Download:** Automatically downloads and installs the appropriate version of ChromeDriver based on the installed version of Chrome.
* **Compatibility Assurance:** Ensures that the ChromeDriver version matches the installed Chrome version, avoiding version mismatches.
* **Easy Integration:** Seamlessly integrates into existing automation scripts, reducing setup and configuration time.
* **Customization:** Offers flexibility to customize the download directory and other aspects of the ChromeDriver installation process.

### Note

* **Current Support:** The current version of `fast-chromedriver-manager` supports only Windows 64-bit systems. Support for other platforms will be added in future releases.

### Usage Example

```
from fast_chromedriver_manager import FastChromeDriverManager

chromedriver_path = FastChromeDriverManager().install()

print(f"ChromeDriver is installed at: {chromedriver_path}")

```

### Usage example with specified Chromedriver path

```
from fast_chromedriver_manager import FastChromeDriverManager

path = 'my_path'
chromedriver_path = FastChromeDriverManager(path).install()

print(f"ChromeDriver is installed at: {chromedriver_path}")
```

### Usage Example with Selenium

```
from selenium import webdriver
from fast_chromedriver_manager import FastChromeDriverManager

# Set up the WebDriver with the path to the ChromeDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=FastChromeDriverManager().install(), options=options)

# Open a website and perform actions
driver.get('https://www.example.com')

# Print the title of the webpage
print(f"Page title is: {driver.title}")

# Close the browser
driver.quit()

```

### Usage Example with Selenium and Service

```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from fast_chromedriver_manager import FastChromeDriverManager

# Set up the WebDriver with the path to the ChromeDriver using Service
service = Service(executable_path=FastChromeDriverManager().install())
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

Fernando Manfré:	 fn.manfre@gmail.com

### Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.
