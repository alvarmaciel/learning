import pytest
from sqlalchemy import select
from ecommerce.domain.entities import Product


@pytest.mark.asyncio
def test_product_entitie_mapping(dbsession):
    # Setup: create the instance class
    product = Product(
        name="pochoclos",
        category="Comestibles",
        price_cents= 1000,
        stock = 10
    )
    # Excecise: add to the db and create a query to the db
    dbsession.add(product)
    dbsession.commit()

    result= dbsession.execute(
        select(Product).where(Product.name=="pochoclos")
    )
    # Verify: the query result with the class
    product_on_db=result.scalar_one()
    assert product_on_db.name == product.name
    assert product_on_db.category == product.category
    assert product_on_db.price_cents == product.price_cents
