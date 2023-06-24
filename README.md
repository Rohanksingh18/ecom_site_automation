# Automated Tests (BE & FE) for an E-Commerce Site

## Description:
Automated tests using Python & Pytest framework to test the Demo Ecom Site.
The site under test is created using WordPress, Woocommerce, and the StoreFront theme. Example: These tests are running on http://localhost:8888/EcomSite


## Prerequisites to run the tests:
1. You must have the E-Commerce site running
2. The site must be created with WordPress & WooCommerce
3. The site must be using the "StoreFront" theme

## Steps for setting up the framework and running the tests

### Clone the code from my public git repository. The link is here:  
```https://github.com/Rohanksingh18/ecom_site_automation.git```

#### Navigate to the cloned directory:
```cd ecom_test```

#### Create a virtual environment and install requirements:
Create a virtual environment:
```python3 -m venv ecom_venv or python -m venv ecom_venv (windows)```

Activate the created virtual environment:
```$ source  ecom_venv/bin/activate``` and for windows ```python ecom_venv\Scripts\activate.bat```

## Install all the requirements in the activated virtual environment:
```python3 -m pip install -r requirements.txt``` or ```python -m pip install -r requirements.txt``` (for windows)

## Set environment variables to run the tests:
This framework requires variables to set the variables, write them in a file and run/source the file. For 'Mac/Linux systems, update and run the 'variables.sh' file; for Windows systems, create a batch ('enev.bat') file to set the variables.

```source variables.sh``` or ```C:\..\enev.bat``` (Windows)

## Run the Tests:
To run all the tests, including FE (Front end) and BE (Back end):
```cd ecom_test```\
```python3 -m pytest tests```\
or ```python -m pytest tests``` (Windows)

To run by the test ID:
```python3 -m pytest -m tcid1``` or ```python -m pytest -m tcid1```(Windows)




