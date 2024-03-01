# Business Logic

* User SignUp-Login with user roles sistem. ✓
* The users can create, read, update, or delete their recipes (CRUD).
* The users can create, read, update, or delete their ingredients (CRUD). ✓
* The user can access a list of all the ingredients in their recipes. ✓
* The user can assign cost to each of their ingredients in diferent weight or volume units. ✓
* The user can save a list of products with their weight per unit.
* The user can maintain a daily production and reduction record for each product.
* The app can calculate:
    * Cost per unit.
    * Cost of each ingredient and its percentage within the recipe.
    * Final price depending on the percentage of the cost within that price.
        | ***Example:*** | $ |
        |-------------------------------------------|-----|
        | Product cost:                             | $12 |
        | Percentage of cost in the final price     | %30 |
        | Final price per unit (100 * 12) / 30  =   | $40 | 
    * Recipe for a specific number of units.
    * Ingredient requisition based on quantities of units for each product.
    * Cost of requisitions.
    * Cost of reductions per day, week or month.  
* The app can display graphs of:
  * Production variation of each product per month or per week.  
  * Requisition variation per month or per week.
  * Reduction variation per day, week, or month.

# Clone and Run the Project Locally

## Clone the Repository:
Open a terminal and use the git clone command to copy the repository to your local machine. Replace <REPOSITORY_URL> with the actual URL of the repository.
```bash
git clone <REPOSITORY_URL>
```
## Create and Activate a Virtual Environment:
Before installing dependencies, it is recommended to create a virtual environment to isolate the project's libraries from the global Python environment. Use the following commands:

### To create a virtual environment (in the project directory):

```bash
  python -m venv venv
```
This command creates a directory named venv containing the virtual environment.

### To activate the virtual environment (depending on the operating system):

On Windows (cmd):
```bash
.\venv\Scripts\activate
```
On Windows (PowerShell):
```bash
.\venv\Scripts\Activate.ps1
```
On Unix or MacOS:
```bash
source venv/bin/activate
```
When the virtual environment is activated, you will see the virtual environment name in the command prompt, indicating that you are working within the virtual environment.

## Installing Dependencies:
After activating the virtual environment, navigate to the project directory and use the Python package manager (pip) to install the dependencies:

```bash
cd project_directory_name
pip install -r requirements.txt
```
These steps ensure that the dependencies are installed within the newly created virtual environment, avoiding conflicts with other globally installed library versions on your system.

## Creating a .env File:

Create a .env file to store the configuration of your database, JWT, email, and CORS credentials. The .env file will be used for managing environment variables in your application. Here's a step-by-step guide on how to do it:

1. Create a file named .env in the root of your project or in the directory where you want to store environment variables.

2. Open the .env file with a text or code editor.

3. Define the environment variables:

  ```bash
  # In this example PostgreSQL is used:

  DB_URL = "postgresql://your_username:your_secret_password@localhost/your_database_name"
  'Make sure to replace your_username, your_secret_password, your_database_name, and other values with your specific configuration.'

  # JSON web token credentials

  JWT_SECRET_KEY = "Secret key for decrypting your JWT's"
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MIN=30 "Duration in minutes that you want the session to last."

  # This email account will be used to send email notifications, verification signup codes, and newsletters to the users.

  EMAIL="example@gmail.com" *Your enterprise email*
  EMAIL_PASSWORD="examplepassword" *This password must be a SMPT password.*
  CHANGE_PASSWORD_ENDPIONT=""

  # Admin user credentials:

  '''With these credentials, a user account with an admin role will be created on the page, allowing access to its administrative panel. This account will be created at the time of database migrations.'''

  NAME="admin user name"
  ADMIN_EMAIL="admin user email"
  PASSWORD="admin user password"

  ```
  4. Save the .env file.

# Migrations:

In Windows, you can open the "Command Prompt" or "PowerShell."
In Unix-based systems, you can open the terminal.

1. Navigate to the directory of the models.py file:

```bash
cd src\db
```
2. Run the script:

Use the python command (or python3 depending on the version) followed by the name of the models.py file.
```bash
python models.py
```
or

```bash
python3 models.py
```
If you're on Windows and don't have python configured as an environment variable, you might need to provide the full path to Python:


```bash
C:\path\to\python.exe models.py
```
*This process assumes you already have Python installed and configured on your system. If not, you will need to install Python before running this migration script. Also, make sure all project dependencies are installed before executing the migration script.*

# Database Diagram:
![alt text](src\utils\static_files\image.png)

*created with:* https://www.eraser.io/

# Testing with pytest:

We utilize the pytest library for testing our application.

## Running Tests:

Running the tests for this application:
1. Navigate to the main directory of your application in the terminal.

2. Run the tests with pytest using the following command:

    ```bash
    pytest
    ```

    For more detailed information during the execution, use the `-v` (verbose) option:

    ```bash
    pytest -v
    ```

    You can also display local variable values in the test output with the `-l` (showlocals) option:

    ```bash
    pytest -v -l
    ```

    harina: 200 g
    mantequilla: 200 gr
    azucar: 200 grms
