from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fast-chromedriver-manager',
    version='1.0.0',
    description='Fast Chromedriver Manager is a Python library that automates the download and installation of the correct version of Chromedriver for your browser, ensuring seamless compatibility. This makes it easier to set up environments for Robotic Process Automation (RPA) applications. Ideal for developers using Selenium or other tools that require Chromedriver, this package guarantees that you always have the right version, eliminating compatibility issues between the browser and the driver.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Fernando N. Manfré',
    author_email='fn.manfre@gmail.com',
    url='https://github.com/fnmanfre/fast-chromedriver-manager',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},   
    install_requires=[
        'certifi==2024.7.4',
        'charset-normalizer==3.3.2',
        'idna==3.7',
        'requests==2.32.3',
        'urllib3==2.2.2'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: OS Independent',  
    ],
    python_requires='>=3.10',
)
