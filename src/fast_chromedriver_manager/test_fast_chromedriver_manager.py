import unittest
import os
from unittest.mock import patch, MagicMock
from fast_chromedriver_manager import FastChromeDriverManager, ChromeVersionError, ChromeDriverDownloadError

class TestFastChromeDriverManager(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_chrome_version_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout="    version    REG_SZ    100.0.4896.60")
        manager = FastChromeDriverManager()
        version = manager.get_chrome_version()
        self.assertEqual(version, "100.0.4896.60")

    @patch('subprocess.run')
    def test_get_chrome_version_no_version_found(self, mock_subprocess):
        mock_subprocess.return_value.stdout = ''
        with self.assertRaises(ChromeVersionError) as context:
            FastChromeDriverManager.get_chrome_version()
        self.assertIn("Unable to determine Chrome version", str(context.exception))
    
    @patch('requests.get')
    def test_download_chromedriver_success(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, content=b'Test content')
        test_dir = './test_download'
        os.makedirs(test_dir, exist_ok=True)
        try:
            manager = FastChromeDriverManager()
            manager.download_chromedriver('http://example.com/chromedriver.zip', test_dir)
            self.assertTrue(os.path.exists(os.path.join(test_dir, 'chromedriver.zip')))
        finally:
            # Clean up the test directory
            for root, dirs, files in os.walk(test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(test_dir)
    
    @patch('requests.get')
    def test_download_chromedriver_failure(self, mock_get):
        mock_get.return_value = MagicMock(status_code=404)
        test_dir = './test_download'
        os.makedirs(test_dir, exist_ok=True)
        try:
            manager = FastChromeDriverManager()
            with self.assertRaises(ChromeDriverDownloadError):
                manager.download_chromedriver('http://example.com/chromedriver.zip', test_dir)
        finally:
            # Clean up the test directory
            for root, dirs, files in os.walk(test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(test_dir)

if __name__ == '__main__':
    unittest.main()
