"""Some Notes on Allocation

A product is identified by a SKU, pronounced "skew," which is short for
stock-keeping unit. Customers place orders. An order is identified by an order
reference and comprises multiple order lines, where each line has a SKU and a
quantity. For example:

    10 units of RED-CHAIR

    1 unit of TASTELESS-LAMP

The purchasing department orders small batches of stock. A batch of stock has a
unique ID called a reference, a SKU, and a quantity.

We need to allocate order lines to batches. When we’ve allocated an order line
to a batch, we will send stock from that specific batch to the customer’s
delivery address. When we allocate x units of stock to a batch, the available
quantity is reduced by x. For example:

    We have a batch of 20 SMALL-TABLE, and we allocate an order line for 2 SMALL-TABLE.

    The batch should have 18 SMALL-TABLE remaining.

We can’t allocate to a batch if the available quantity is less than the quantity
of the order line. For example:

    We have a batch of 1 BLUE-CUSHION, and an order line for 2 BLUE-CUSHION.

    We should not be able to allocate the line to the batch.

We can’t allocate the same line twice. For example:

    We have a batch of 10 BLUE-VASE, and we allocate an order line for 2 BLUE-VASE.

    If we allocate the order line again to the same batch, the batch should still have an available quantity of 8.

Batches have an ETA if they are currently shipping, or they may be in warehouse
stock. We allocate to warehouse stock in preference to shipment batches. We
allocate to shipment batches in order of which has the earliest ETA.

"""
from allocator.domain.models import LineItem, Batch
from datetime import date
import pytest

# @pytest.fixture
# def give_batch(sku:str, quantity: int, in_warehouse: bool, eta:int) -> Batch:
#     return Batch(sku="sku", quantity=quantity, in_warehouse=in_warehouse, eta=eta)

# allocate order lines to batches
def test_allocate_order_lines_to_batches():
    # Setup
    # get orders
    order_line_item = LineItem("order-ref", "SMALL-TABLE", 2)
    # get bacthes
    batch = Batch('batch_001', "SMALL-TABLE", quantity=20, eta=date.today())
    # Excercise
    # Allocate line itens
    batch.allocate(order_line_item)
    # Verify
    assert batch.quantity == 18

# can't allocate to a batch with less available quantity
# def test_cant_allocate_to_smaller_batches():
#     # Setup
#     # get orders
#     order = Order([LineItem(sku="SMALL-TABLE", quantity= 2)])
#     # get bacthes
#     batches = [give_batch("SMALL-TABLE", 1, False, 10)]
#     # Excercise
#     # Allocate line itens
#     allocator(order, batches)
#     # Verify
#     batches[0].quantity = 1

# # can't allocate the same line twice
# def cant_allocate_the_same_line_twice():
#     # Setup
#     # get orders
#     order = Order([LineItem(sku="SMALL-TABLE", quantity= 2)])
#     # get bacthes
#     batches = [give_batch("SMALL-TABLE", 20, False, 10)]
#     # Excercise
#     # Allocate line itens
#     allocator(order, batches)
#     allocator(order, batches)
#     # Verify
#     batch[0].quantity = 18

# # Allocate first in warehause, then in batches by ETA
# def allocate_first_in_warehouse():
#     # Setup
#     # get orders
#     orders = [Order([LineItem(sku="SMALL-TABLE", quantity=2)]),
#               Order([LineItem(sku="BLUE-CUSHION", quantity=1)])]
#     # get bacthes
#     batches = [give_batch("SMALL-TABLE", 20, False, 10),
#                give_batch("SMALL-TABLE", 20, True, 10),
#                give_batch("BLUE-CUSHION", 10, False, 10),
#                give_batch("BLUE-CUSHION", 10, False, 9),]
#     # Excercise
#     # Allocate line itens
#     allocator(order, batchess)
#     # Verify
#     batches[0].quantity = 20
#     batches[1].quantity = 18
#     batches[2].quantity = 10
#     batches[3].quantity = 9
