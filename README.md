# Requirements

* User SignIn-Login sistem. ✓
* The users can create, read, update, or delete their recipes (CRUD).
* The user can access a list of all the ingredients in their recipes.
* The user can assign a cost per kg to each of their ingredients.
* The user can save a list of products with their weight per unit.
* The user can maintain a daily production and reduction record for each product.
* The app can calculate:
    * Cost per unit.
    * Cost of each ingredient and its percentage within the recipe.
    * Final price depending on the percentage of the cost within that price.
        | ***Example:*** | $ |
        |-------------------------------------------|-----|
        | Product cost:                             | $12 |
        | Percentage of cost in the final price     | 30% |
        | Final price per unit (100 * 12) / 30 =    | $40 | 
    * Recipe for a specific number of units.
    * Ingredient requisition based on quantities of units for each product.
    * Cost of requisitions.
    * Cost of reductions per day, week or month.  
* The app can display graphs of:
  * Production variation of each product per month or per week.  
  * Requisition variation per month or per week.
  * Reduction variation per day, week, or month.


# Creating a .env File for Storing PostgreSQL Database Credentials

Create a .env file to store the configuration of your local PostgreSQL database. The .env file is a common practice for managing environment variables in your application. Here's a step-by-step guide on how to do it:

* Create a file named .env in the root of your project or in the directory where you want to store environment variables.

* Open the .env file with a text or code editor.

* Define the environment variables you need for your database configuration. In your case, you need to define variables for the     PostgreSQL database username and password. For example:
  ```
  DB_URL = "postgresql://your_username:your_secret_password@localhost/your_database_name"

  JWT_SECRET = *Secret key for decrypting youre JWT's* 
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MIN=30
  ```
  *Make sure to replace your_username, your_secret_password, your_database_name, and other values with your specific configuration.*

* Save the .env file.


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


