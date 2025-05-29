# Ecommerce API

A Django REST Framework-based ecommerce API that provides product management and shopping cart functionality with JWT authentication.

## Features

- Product CRUD operations
- Shopping cart management
- User authentication with JWT tokens
- Paginated API responses
- Admin-only product management
- User-specific cart operations

## Technology Stack

- **Backend**: Django 5.2.1
- **API Framework**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite 
- **Python**: 3.8+

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Janjitya/ecommerce_project_task.git
   cd ecommerce_project_task
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   cd ecommerce_project
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. You'll need to obtain access and refresh tokens to use protected endpoints.

### Get JWT Tokens

**Endpoint**: `POST /api/token/`

**Request Body**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response**:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token

**Endpoint**: `POST /api/token/refresh/`

**Request Body**:
```json
{
    "refresh": "your_refresh_token"
}
```

### Using JWT Token

Include the access token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## API Endpoints

### Products

#### 1. List All Products
- **URL**: `GET /api/products/`
- **Permission**: Public (no authentication required)
- **Description**: Retrieve a paginated list of all products

**Response Example**:
```json
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "product_name": "Laptop",
            "description": "High-performance laptop",
            "price": "999.99",
            "created_at": "2024-01-01T12:00:00Z"
        }
    ]
}
```

#### 2. Create Product
- **URL**: `POST /api/products/create/`
- **Permission**: Admin only
- **Description**: Create a new product

**Request Body**:
```json
{
    "product_name": "Smartphone",
    "description": "Latest model smartphone",
    "price": "699.99"
}
```

#### 3. Get/Update/Delete Product
- **URL**: `GET/PUT/PATCH/DELETE /api/product/<id>/`
- **Permission**: Admin only
- **Description**: Retrieve, update, or delete a specific product

**Update Request Body**:
```json
{
    "product_name": "Updated Product Name",
    "description": "Updated description",
    "price": "799.99"
}
```

### Shopping Cart

#### 1. View Cart Items
- **URL**: `GET /api/cart/`
- **Permission**: Authenticated users only
- **Description**: Get paginated list of user's cart items

**Response Example**:
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "product": 1,
            "product_price": "999.99",
            "quantity": 2,
            "total_price": "1999.98",
            "added_at": "2024-01-01T12:00:00Z",
            "user": 1
        }
    ]
}
```

#### 2. Add to Cart
- **URL**: `POST /api/cart/`
- **Permission**: Authenticated users only
- **Description**: Add a product to cart or increment quantity if already exists

**Request Body**:
```json
{
    "product_id": 1
}
```

#### 3. Update Cart Item Quantity
- **URL**: `PUT /api/cart/<cart_item_id>/`
- **Permission**: Authenticated users only
- **Description**: Update quantity of a specific cart item

**Request Body**:
```json
{
    "quantity": 3
}
```

#### 4. Delete Cart Item
- **URL**: `DELETE /api/cart/<cart_item_id>/`
- **Permission**: Authenticated users only
- **Description**: Remove a specific item from cart

**Response**:
```json
{
    "message": "Cart item deleted successfully"
}
```

#### 5. Clear Cart
- **URL**: `DELETE /api/cart/clear/`
- **Permission**: Authenticated users only
- **Description**: Remove all items from user's cart

**Response**:
```json
{
    "message": "cart cleared"
}
```

#### 6. Get Cart Total
- **URL**: `GET /api/cart/total/`
- **Permission**: Authenticated users only
- **Description**: Get total price and item count for user's cart

**Response Example**:
```json
{
    "cart_total": "2999.97",
    "item_count": 3
}
```

## Testing the API

### Using Postman

1. Import the collection by creating requests for each endpoint
2. Set up environment variables for base URL and tokens
3. Use the JWT token in the Authorization tab (Bearer Token)

## Project Structure

```
ecommerce_project/
├── api/
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   └── urls.py           # API URL patterns
├── cart/
│   └── models.py         # Product and CartItem models
├── ecommerce_project/
│   ├── settings.py       # Django settings
│   └── urls.py           # Main URL configuration
├── requirements.txt      # Python dependencies
└── manage.py             # Django management script
```

## Key Features Explained

### Cart Functionality
- Users can add products to their cart
- Duplicate products increment quantity instead of creating new cart items
- Cart items store the product price at the time of addition
- Automatic calculation of total prices

### Authentication & Permissions
- JWT tokens with 60-minute access token lifetime
- Refresh tokens with 1-day lifetime
- Admin-only access for product management
- User-specific cart isolation

### Pagination
- Default page size of 5 items
- Consistent pagination across list endpoints



