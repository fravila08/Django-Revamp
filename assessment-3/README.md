# Assessment 3: Django E-commerce Business API

## Requirements

Build an e-commerce API with a shopping cart feature. 
- Your API should be a Django application that returns JsonResponses for the corresponding inputs.
- Using Django ORM/psycopg2/Postgres:
    - Create a model named `Category` to store your different Categories. Using what you have learned, use your best judgment on how to define each of these fields:
        - `title` - a unique name
    - Create a model named `Product` to store product data. It should have the following fields. Using what you have learned, use your best judgment on how to define each of these fields:
        - `id` - a unique id.
        - `name` - name of the product.
        - `category` - the `id` of the Category this product belongs to.
        - `price` - the product price.
    - Create a model named `CartItem` to store the shopping cart. It should have the following fields. Using what you have learned, use your best judgment on how to define each of these fields:
        - `product_id` - the `id` of the product in the cart.
        - `quantity` - the number of items of the product in the cart.
    - If necessary or desired create whatever other fields on these models, or whatever other models you want.
    - **Through whatever means you prefer, insert some fake data into your database. You should have at least 3 different products, and at least two different categories.**

Here is an example of Category:
| id  | title  | 
| --- | -------|
| 1  | personal_care | 

Here is an example Product:
| id  | name   | category      | cost |
| --- | -------|-------------- |------|
| 1  | shampoo | 1             | 4.5 |
| 2  | pencil  | 3             | 1.50 |

Here is an example CartItem:
| id | product_id  | quantity   |
| --| ----------- | -----------|
| 1 | 1           | 3          |
| 2 | 2           | 10         | 


Your website must allow the user to search for and browse products, and add products to their shopping cart.

### Required Routing and Responses

- GET
    - `products/` name = `products`
        - Returns `{'all_products':list of product instances as the value.}`
    - `cart/` name = `cart`
        - Returns {'cart_items' : products in cart, 'cart_total': total price for all items in cart}
    - `products/<str:name>/` name = `product`
        - parameter `name` corresponds to a `Products` name
        - Returns `{'product': product matching product name}`
    - `category/<str:title>/` name = `category`
        - parameter `title` corresponds to a `Category` title
        - returns `{f"category_title": All products with this category}`
- PUT
    - `cart_item/<int:id>/<str:operation>/`  name = `cart_item_edit`
        - parameter `id` corresponds to a `Product` id
        - patameter `operation` corresponds to either [ add | drop ]
        - returns `{f"product_name": product quantity}`

- POST / DELETE 
    - `cart_item/<int:id>/` name = `cart_item`
        - parameter `id` corresponds to a `Product` id
        - Returns on POST `{'success':f"{product.name} has been added to your cart"}` or `{'Failure': "Item either does not exist or is already in your cart"}`
        - Returns on DELETE `{"success": f"{name} has been deleted"}`


## Important Grading Information
- Your assessment, regardless of completion status, must be submitted by the deadline. 

- You need to get a 75% or better to pass. (You must pass all assessments in order to graduate Code Platoon's program.)
- If you fail the assessment, you have can retake it once to improve your score. For this assessment... 
  - *5% penalty*: If you complete and submit the retake **within one week** of receiving your grade.
  - *10% penalty*: If you complete and submit the retake after one week of receiving your grade.

## Rules / Process
- This test is fully open notes and open Google, but is not to be completed with the help of any other student/individual.