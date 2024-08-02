This project is in response to an interview backend project.
This project aims to solve a 

To gain access
start by going to the registration route
  /admin/register

By default you will have admin privileges so you can check out how the project works

When you are logged in, the possibilities are as follows
  - Register (/admin/register)
  - Login (/admin/login)
  - Log out (/admin/logout)
  - Add category (/admin/category/add)
  - All categories (/admin/category/all)
  - Delete category (/admin/category/delete/<id>)
  - Add product (/admin/product/add)
  - Edit product (/admin/product/<product_id>/updtae)
  - Delete product (/admin/product/<product_id>/delete)
  - Fetch all products/menu (/admin/product/all)
  - Fetch single product/menu (/admin/product/<product_id>/view)
  - Fetch all users (/admin/users)
  - Add user (/admin/users/add)
  - Delete user (/admin/users/delete/<id>)
  - Edit user (/admin/users/edit/<id>)
  - View Orders (/admin/orders)
  - Pending orders (/admin/orders/pending)
  - Failed orders (/admin/orders/failed)
  - Successful orders (/admin/orders/success)
  - Delete order (/admin/order/delete/<order_id>)
  - View order (/admin/order/view/<order_id>)


For the Api which will connect to the front end, the possibilities are as follows
  - Register (/register)
  - Login (/login)
  - All menu (/menus)
  - Fetch Single item (/menus/<id>)
  - Fetch Drinks (/menus/drinks)
  - Fetch discounted items (/menus/discounted)
  - View profile (/profile)

The errors are handled accordingly, and a corresponding error message will be displayed
