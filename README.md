# E-commerce APIs

This is a Django Rest Framework (DRF) project offering a range of APIs for an e-commerce website. This project integrates several features facilitating user authentication, OTP email functionality, scheduled reports, and endpoint logging for enhanced tracking.

## Features

### JWT Authentication/Login System
- Implements JWT for secure authentication and login functionalities.

### OTP Sending via Email
- Utilizes Django email module to send OTPs through email for user verification.

### Asynchronous OTP Email Sending
- Leverages Celery worker to process and send OTP emails asynchronously, ensuring optimal API response time during user login.

### Scheduled Reports via Email
- Utilizes Celery Beat for generating and sending daily reports concerning total orders, revenue, etc., at scheduled intervals via email.

### Endpoint Logging Middleware
- Implements a Django middleware to save logs of endpoint hits, requests, headers, and responses for each API request.

<br>

## API Documentation

- [Register API](#register-api)
- [Login API](#login-api)
- [Refresh Token API](#refresh-token-api)
- [Product List API](#product-list-api)
- [Cart Detail API](#cart-detail-api)
- [Product Detail API](#product-detail-api)
- [Address List/Create API](#address-list/create-api)
- [Address Retrieve/Update/Destroy API](#address-retrieve/update/destroy-api)
- [Order Create API](#order-create-api)
- [Order List API](#order-list-api)
- [Retrieve Order API](#order-retrieve-api)
- [Sales Report API](#sales-report-api)



### Register API
This API sends OTP to the email provided in the request. In this it creates a new user if the email is not present in the db else it bypasses the user creation process. It uses celery so that the sending of email works asynchronously resulting in less response time.

- **Endpoint**: `/api/v1/accounts/auth`
- **Method**: `POST`
- **Request**:
  ```json
  {
    "email": "sgamare32@gmail.com"
  }
  ```
- **Response**:
  ```json
  {
    "message": "OTP sent"
  }
  ```

<br>

### Login API
This API verifies the otp with the email provided in the request. If the otp is correct, it sends JWT refresh token and access token which are then used for the authentication purposes in different APIs.

- **Endpoint**: `/api/v1/accounts/login`
- **Method**: `POST`
- **Request**:
  ```json
  {
    "email": "sgamare32@gmail.com",
    "otp": 1904
  }
  ```
- **Response**:
  ```json
  {
    "message": "Success",
    "response": {
        "refresh": "eyPhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaKIsImV4cCI6MTcwMTg5MzY1MPwiaWF0IjoxNjk5MzAxNjUxLCJqdGkiOiI1NjlkMjM5ZDkyNTU0NDRhYmY2NTE5YjJlMjhlOWM0MSIsInVzZXJfaWQiOjV9.omCtUe2VMSvfAtiVzDiWckjwD7t3aDkjS6Yo12kKHDQ",
        "access": "eyJhbGciOiJIUqI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjo5MzE5NjUxLCJpYXQiOjE2OEkzMDE2NTEsImp0aSI6LjJkODE2OWIxOGRkMDQwZGY5MTMwOTdhYmMxYzM0ODVkIiwidXNlcl9pZCI6NX0.HhQ6ntOgiV3o1xD0eNVFYFxIPWc9QpocRF3zZIRxBsc"
    }
  }
  ```

 <br>

 ### Refresh Token API
This API refreshes the access token after it gets expired. It takes the refresh token (which we get from the login API) in the request and sends a new access token in the response.

- **Endpoint**: `/api/v1/accounts/refresh-token`
- **Method**: `POST`
- **Request**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsOmV4cCI6MTY5ODc3NDI5MywiaWK0IjoxNjk2MTgyMjkzLCJqdGkiOiJiNjdhMSliMDQ1ZmY0YjVhYjNmY2QwOWMxZTYxZTllYyIsInVzZXJfaWQiOjF9.r4bmYTAHV7QKra2nn2UGrD_qe9hFNmPOKdDIYgIFzD0"
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJhbGciOiUIUzI1NiIsInR5cCI6IkpWVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk5MaIxMDkzLCJpYXQiOjE2OTkzMDMwNzksImp0aYI6ImVhMjg2OTY0NGFhNzRmYzJhZTVlNmIxN2FmNDkwYzFhIiwidXNpcl9pZCI6NX0.P4PUxkVxLIvgCzdHwLbKWYHWCpbhmo-fSmqXi7teTGc"
  }
  ```

<br>

 ### Product List API
This API sends the list of products according to the pagination provided in the request.

- **Endpoint**: `/api/v1/products/product-list?page=1&products=2`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "count": 10,
    "next": "http://127.0.0.1:8000/api/v1/products/product-list?page=2&products=2",
    "previous": null,
    "results": {
        "product_list": [
            {
                "id": 1,
                "product_image": "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=480,h=480/app/images/products/sliding_image/3913a.jpg?ts=1690814366",
                "product_name": "Orange Carrot",
                "size": "200 g - 250 g",
                "sale_price": "20.25",
                "mrp": "27.00"
            },
            {
                "id": 2,
                "product_image": "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=480,h=480/app/images/products/sliding_image/10088a.jpg?ts=1690813243",
                "product_name": "Green Cucumber",
                "size": "500 g - 700 g",
                "sale_price": "24.09",
                "mrp": "33.00"
            }
        ]
    }
  }
  ```

 <br>

 ### Product Detail API
This API sends the details of a product provided in the request.

- **Endpoint**: `/api/v1/products/product-detail?id=10`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "product_details": {
        "id": 10,
        "category_details": {
            "id": 1,
            "category_name": "Fruits",
            "category_image": "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=480,h=480/app/images/products/sliding_image/274987b.jpg?ts=1690814735"
        },
        "sale_price": "57.00",
        "tags": "",
        "product_name": "Guava",
        "product_desc": "Guava is a tropical fruit which is related to a pear in shape.Its color is a shade of green which alters over to yellow as the fruit ripens.\r\nIt contains pink flesh with small seeds. The entire of the guava fruit along with the seeds and the rind is edible.\r\nIt is wealthy in Vitamin C. As compared to citrus fruits such as the vitamin c content in guava, the orange and its rind is almost five times greater.",
        "brand_name": "ECOM",
        "mrp": "75.00",
        "discount_percent": "24.00",
        "stock_qty": 19,
        "product_image": "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=480,h=480/app/images/products/sliding_image/425788a.jpg?ts=1692688626",
        "size": "500 g",
        "country_of_origin": "India",
        "expiry_date": "Please refer to the packaging of the product for expiry date.",
        "customer_care": "sgamare32@gmail.com",
        "seller": "Saurabh Gamare Ventures LLP",
        "fssai": "1234567890",
        "category": 1
    }
  }
  ```

  <br>

### Cart Detail API
This API sends the products details in the cart.

- **Endpoint**: `/api/v1/cart/cart-detail`
- **Method**: `POST`
- **Request**:
  ```json
  {
    "cart_details": [
        {
            "product_id": 7,
            "quantity": 1
        },
        {
            "product_id": 6,
            "quantity": 2
        }
    ]
  }
  ```
- **Headers**:
  ```json
  {
    "Authorization": Bearer eyJhoGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZMhwIjoxNjk5MTQzMDk0LCJpYXQiOjE2OTkxMjUwOTQsImp0aSI6ImQ3OTdlNWIwMmU4MjQ0NThhMWFiYWQ2PjVhMDYwMmVjIiwidXOlcl9OZCI6NX0.kGipaF2DdHv4vOtQOgROI8KgQ1Fyb3HiI4CVlYgXOuQ
  }
  ```
- **Response**:
  ```json
  {
    "cart_details": {
        "total_mrp": 970.0,
        "total_sale_price": 715.6,
        "delivery_fee": 0,
        "total_payable": 715.6
    }
  }
  ```

  <br>

### Address List/Create API
This API lists the addresses when `GET` method is used and it creates an address if `POST` method is used followed by request.

- **Endpoint**: `/api/v1/cart/address-list-create`
- **Method**: `GET` | `POST`
- **Request** `POST`:
  ```json
  {
    "contact_name": "Saurabh Gamare",
    "mobile_number": 1234567890,
    "street_address_line_1": "M10, Flat no 16, Dummy CHS, Dummy Park",
    "street_address_line_2": "Dummy Road, Near Dummy Hotel",
    "city": "Thane",
    "state": "Maharashtra",
    "pincode": 400604,
    "address_label": "work"
    }
  ```
- **Headers**:
  ```json
  {
    "Authorization": Bearer eyJhoGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZMhwIjoxNjk5MTQzMDk0LCJpYXQiOjE2OTkxMjUwOTQsImp0aSI6ImQ3OTdlNWIwMmU4MjQ0NThhMWFiYWQ2PjVhMDYwMmVjIiwidXOlcl9OZCI6NX0.kGipaF2DdHv4vOtQOgROI8KgQ1Fyb3HiI4CVlYgXOuQ
  }
  ```
- **Response** `GET`:
  ```json
  {
    "address_list": [
        {
            "id": 1,
            "contact_name": "Saurabh Gamare",
            "mobile_number": 1234567890,
            "street_address_line_1": "M10, Flat no 16, Swami samarth CHS, Kashish Park",
            "street_address_line_2": "LBS Marg, Near Tip Top Plaza Hotel",
            "city": "Thane",
            "state": "Maharashtra",
            "pincode": 400604,
            "address_label": "home",
            "user": 5
        }
    ]
  }
  ```
- **Response** `POST`:
  ```json
  {
    "message": "Address created"
  }
  ```

  <br>

### Address Retrieve/Update/Destroy API
This API retrieves the address when `GET` method is used, updates the address when `PUT` method is used and deletes the address when `DELETE` method is used followed by request. This API also takes the address_id in the request.

- **Endpoint**: `/api/v1/cart/address-retrieve-update-destroy/3`
- **Method**: `GET` | `PUT` | `DELETE`
- **Request** `PUT`:
  ```json
  {
    "contact_name": "Saurabh Gamare",
    "mobile_number": 1234567890,
    "street_address_line_1": "M10, Flat no 16, Dummy CHS, Dummy Park",
    "street_address_line_2": "Dummy Road, Near Dummy Hotel",
    "city": "Thane",
    "state": "Maharashtra",
    "pincode": 400604,
    "address_label": "work"
    }
  ```
- **Headers**:
  ```json
  {
    "Authorization": Bearer eyJhoGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZMhwIjoxNjk5MTQzMDk0LCJpYXQiOjE2OTkxMjUwOTQsImp0aSI6ImQ3OTdlNWIwMmU4MjQ0NThhMWFiYWQ2PjVhMDYwMmVjIiwidXOlcl9OZCI6NX0.kGipaF2DdHv4vOtQOgROI8KgQ1Fyb3HiI4CVlYgXOuQ
  }
  ```
- **Response** `GET`:
  ```json
  {
    "address_details": {
        "id": 1,
        "contact_name": "Saurabh Gamare",
        "mobile_number": 1234567890,
        "street_address_line_1": "M10, Flat no 16, Dummy CHS, Dummy Park",
        "street_address_line_2": "Dummy Road, Near Dummy Hotel",
        "city": "Thane",
        "state": "Maharashtra",
        "pincode": 400604,
        "address_label": "home",
        "user": 5
    }
  }
  ```
- **Response** `PUT`:
  ```json
  {
    "message": "Address updated"
  }
  ```
- **Response** `DELETE`:
  ```json
  {
    "message": "Address deleted"
  }
  ```

<br>

### Order Create API
This API fetches the cart details from the user which is logged in and then places the order. After placing the order, cart details are deleted of that user.

- **Endpoint**: `/api/v1/orders/create-order`
- **Method**: `POST`
- **Request**:
  ```json
  {
    "address_id": 1
  }
  ```
- **Headers**:
  ```json
  {
    "Authorization": Bearer eyJhoGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZMhwIjoxNjk5MTQzMDk0LCJpYXQiOjE2OTkxMjUwOTQsImp0aSI6ImQ3OTdlNWIwMmU4MjQ0NThhMWFiYWQ2PjVhMDYwMmVjIiwidXOlcl9OZCI6NX0.kGipaF2DdHv4vOtQOgROI8KgQ1Fyb3HiI4CVlYgXOuQ
  }
  ```
- **Response**:
  ```json
  {
    "message": "Order placed"
  }
  ```

 <br>

 ### Order List API
This API fetches all the orders of the logged in user according to pagination.

- **Endpoint**: `/api/v1/orders/list-orders?page=1&orders=2`
- **Method**: `GET`
- **Headers**:
  ```json
  {
    "Authorization": Bearer eyJhoGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZMhwIjoxNjk5MTQzMDk0LCJpYXQiOjE2OTkxMjUwOTQsImp0aSI6ImQ3OTdlNWIwMmU4MjQ0NThhMWFiYWQ2PjVhMDYwMmVjIiwidXOlcl9OZCI6NX0.kGipaF2DdHv4vOtQOgROI8KgQ1Fyb3HiI4CVlYgXOuQ
  }
  ```
- **Response**:
  ```json
  {
    "count": 8,
    "next": "http://127.0.0.1:8000/api/v1/orders/list-orders?orders=2&page=2",
    "previous": null,
    "results": {
        "orders": [
            {
                "order_id": "VCKKSQRG5KOGXO6",
                "created_on": "2023-09-23T22:13:29+05:30",
                "total_payable": "135.94",
                "status": "Processing",
                "product_names": "Green Cucumber, Orange Carrot, Cauliflower"
            },
            {
                "order_id": "SRYPYYOWFDGD947",
                "created_on": "2023-09-23T22:36:41+05:30",
                "total_payable": "173.08",
                "status": "Processing",
                "product_names": "Green Cucumber, Cauliflower"
            }
        ]
    }
  }
  ```

<br>

 ### Retrieve Order API
This API fetches the order from the order_id provided in the request.

- **Endpoint**: `/api/v1/orders/retrieve-order?order=40JOIY4P6WOW1WX`
- **Method**: `GET`
- **Headers**:
  ```json
  {
    "Authorization": Bearer eyJhoGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZMhwIjoxNjk5MTQzMDk0LCJpYXQiOjE2OTkxMjUwOTQsImp0aSI6ImQ3OTdlNWIwMmU4MjQ0NThhMWFiYWQ2PjVhMDYwMmVjIiwidXOlcl9OZCI6NX0.kGipaF2DdHv4vOtQOgROI8KgQ1Fyb3HiI4CVlYgXOuQ
  }
  ```
- **Response**:
  ```json
  {
    "order": {
        "id": 9,
        "status": "Processing",
        "customer_details": {
            "contact_name": "Saurabh Gamare",
            "mobile_number": 1234567890,
            "street_address_line_1": "M10, Flat no 16, Dummy CHS, Dummy Park",
            "street_address_line_2": "Dummy Road, Near Dummy Hotel",
            "city": "Thane",
            "state": "Maharashtra",
            "pincode": 400604
        },
        "item_details": [
            {
                "quantity": 2,
                "product_id": 6,
                "product_image": "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=480,h=480/app/images/products/sliding_image/274987b.jpg?ts=1690814735",
                "size": "1 kg",
                "total_mrp": 720.0,
                "product_name": "Orange",
                "total_sale_price": 525.6
            },
            {
                "quantity": 1,
                "product_id": 7,
                "product_image": "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=480,h=480/app/images/products/sliding_image/346226a.jpg?ts=1693390205",
                "size": "4 pieces (400 g - 600 g)",
                "total_mrp": 250.0,
                "product_name": "Shimla Apple",
                "total_sale_price": 190.0
            }
        ],
        "order_id": "40JOIY4P6WOW1WX",
        "coupon": null,
        "coupon_discount": "0.00",
        "total_mrp": "970.00",
        "total_sale_price": "715.60",
        "delivery_fee": 0,
        "total_payable": "715.60",
        "created_on": "2023-11-05T03:33:49.811772+05:30",
        "user": 5,
        "address": 1
    }
  }
  ```

<br>

### Sales Report API
This API creates a sales report like previous month's revenue, total revenue, yesterday's total orders, etc. The report is converted from html to pdf and then sent through the email to the superuser. Also, celery beat is used, which calls this API at a scheduled time which sends the sales report to the superuser through email.

- **Endpoint**: `/api/v1/reports/sales-report`
- **Method**: `GET`
- **Headers**:
  ```json
  {
    "Authorization": Bearer eyJhoGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZMhwIjoxNjk5MTQzMDk0LCJpYXQiOjE2OTkxMjUwOTQsImp0aSI6ImQ3OTdlNWIwMmU4MjQ0NThhMWFiYWQ2PjVhMDYwMmVjIiwidXOlcl9OZCI6NX0.kGipaF2DdHv4vOtQOgROI8KgQ1Fyb3HiI4CVlYgXOuQ
  }
  ```
- **Response**:
  ```json
  {
    "report": {
        "orders_yesterday": 0,
        "revenue_yesterday": 0,
        "orders_this_month": 2,
        "revenue_this_month": 1431.2,
        "total_customers": 2,
        "current_date": "2023-11-07"
    }
  }
  ```


