from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from sqlalchemy.orm import Session
from ..models import Product

@view_config(route_name='products', request_method='POST', renderer='json')
def create_product(request):
    """ Create a new product record in the database. """
    db = request.dbsession
    data = request.json_body

    # Validate input data
    if not all(key in data for key in ('name', 'description', 'price')):
        raise HTTPBadRequest('Missing required fields')

    # Create a new Product object with the input values
    product = Product(name=data['name'], description=data['description'], price=data['price'])

    # Add the new product to the database
    db.add(product)
    db.flush()

    # Return the newly created product as JSON
    return product.to_dict()

@view_config(route_name='products', request_method='GET', renderer='json')
def get_products(request):
    """ Retrieve a list of product records from the database. """
    db = request.dbsession
    skip = request.params.get('skip', 0)
    limit = request.params.get('limit', 100)

    # Retrieve a list of products from the database
    products = db.query(Product).offset(skip).limit(limit).all()

    # Return the list of products as JSON
    return [product.to_dict() for product in products]

@view_config(route_name='product', request_method='GET', renderer='json')
def get_product(request):
    """ Retrieve a product record from the database by ID. """
    db = request.dbsession
    product_id = request.matchdict['id']

    # Retrieve the product from the database
    product = db.query(Product).filter(Product.id == product_id).first()

    # Return the product as JSON, or raise a 404 error if it doesn't exist
    if product is not None:
        return product.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='product', request_method='PUT', renderer='json')
def update_product(request):
    """ Update an existing product record in the database. """
    db = request.dbsession
    product_id = request.matchdict['id']
    data = request.json_body

    # Retrieve the product from the database
    product = db.query(Product).filter(Product.id == product_id).first()

    # Update the product with the input values
    if product is not None:
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']

        # Commit the changes to the database
        db.commit()

        # Return the updated product as JSON
        return product.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='product', request_method='DELETE', renderer='json')
def delete_product(request):
    """ Delete a product record from the database by ID. """
    db = request.dbsession
    product_id = request.matchdict['id']

    # Retrieve the product from the database
    product = db.query(Product).filter(Product.id == product_id).first()

    # Delete the product from the database
    if product is not None:
        db.delete(product)
        db.commit()

        # Return a success message as JSON
        return {'message': 'Product deleted'}
    else:
        raise HTTPNotFound()