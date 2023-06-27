
# Automated Tests (BE & FE) for an E-Commerce Site

## Description

This repository contains automated tests using Python and the Pytest framework to test a Demo E-Commerce Site. The site under test is created using WordPress, WooCommerce, and the StoreFront theme. The tests are designed to run on the URL [http://localhost:8888/EcomSite](http://localhost:8888/EcomSite).

## Prerequisites to Run the Tests

To successfully run the tests, ensure the following prerequisites are met:

- The E-Commerce site is up and running.
- The site has been created using WordPress and WooCommerce.
- The site is using the "StoreFront" theme.

## Steps for Setting Up the Framework and Running the Tests

1. Clone the code from the public Git repository. The repository link is:

   [https://github.com/Rohanksingh18/ecom_site_automation.git](https://github.com/Rohanksingh18/ecom_site_automation.git)

2. Navigate to the cloned directory:

   ```
   cd ecom_test
   ```

3. Create a virtual environment and install the required packages:

   - Create a virtual environment:
     - Mac/Linux: `python3 -m venv ecom_venv`
     - Windows: `python -m venv ecom_venv`

   - Activate the created virtual environment:
     - Mac/Linux: `$ source ecom_venv/bin/activate`
     - Windows: `python ecom_venv\Scripts\activate.bat`

   - Install the required packages in the activated virtual environment:
     ```
     python3 -m pip install -r requirements.txt
     ```

4. Set the environment variables to run the tests:

   - This framework requires setting environment variables. Write the necessary variables in a file and then run or source the file.
   - For Mac/Linux systems, update and run the `variables.sh` file.
   - For Windows systems, create a batch (`enev.bat`) file to set the variables.

     - Mac/Linux: `source variables.sh`
     - Windows: `C:\..\enev.bat`

5. Run the Tests:

   - To run all the tests, including Front-end (FE) and Back-end (BE), navigate to the `ecom_test` directory and execute the following command:
     - Mac/Linux: `python3 -m pytest tests`
     - Windows: `python -m pytest tests`

   - To run a specific test by test ID, use the following command:
     - Mac/Linux: `python3 -m pytest -m tcid1`
     - Windows: `python -m pytest -m tcid1`

Note: Modify the commands based on your operating system and specific requirements.

---

Feel free to adjust the instructions and content as necessary, adding any additional information or clarifications.




