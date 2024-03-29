# DB Tables

## Users Table:

* user_id (PK)
* username
* email
* password_hash
* creation_date
* role
* confirmation_code

## Recipes Table:

* recipe_id (PK)
* user_id (FK to Users Table)
* recipe_name
* category
* user
* ingredients

## Ingredients Table:

* ingredient_id (PK)
* user_id
* ingredient_name
* cost
* unit_of_meassure
* has_gluten
* is_vegan
* supplier
* brand
* recipes

## Share Recipes Table:

* share_id (PK)
* from_user_id (FK to Users Table)
* to_user_id (FK to Users Table)
* recipe_id (FK to Recipes Table)
* share_date (Date)


## Ingredients_Recipes Table (Intermediate Table):

* ingredient_recipe_id (PK)
* recipe_id (FK to Recipes Table)
* ingredient_id (FK to Ingredients Table)
* weight

___
## Examples:

***Users_Table***

| user_id | name     | email               | password_hash
|---------|----------|---------------------|----------
| 1       | user1    | user1@example.com   | 2w3er456hsg
| 2       | user2    | user2@example.com   | 6w3er45123

***Recipes_Table***

| recipe_id | user_id (FK to Users table) | recipe_name    | product_weight | unit_of_meassure |
|-----------|-----------------------------|----------------|----------------|------------------|
| 1         | 1                           | Bread Recipe   |       80       | g                |
| 2         | 1                           | Cake Recipe    |      500       | g                |
| 3         | 1                           | Cookie Recipe  |      100       | g                |
| 4         | 2                           | Pie Recipe     |      500       | g                |
| 5         | 2                           | Muffin Recipe  |       80       | g                |

***Ingerdient_Recipe Table example:***

| ingredient_recipe_id | recipe_id | ingredient_id | weight | unit_of_meassure |
|----------------------|-----------|---------------|--------|------------------|
| 1                    | 1         | 1             | 500    | g                |
| 3                    | 1         | 3             | 200    | g                |
| 2                    | 1         | 2             | 300    | g                |
| 4                    | 2         | 1             | 400    | g                |
| 5                    | 2         | 4             | 150    | g                |
| 6                    | 2         | 5             | 100    | g                |
| 7                    | 2         | 6             | 50     | g                |
