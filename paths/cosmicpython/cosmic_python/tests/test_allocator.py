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
from allocator.domain.models import LineItem, Batch, allocate
from datetime import date, timedelta
import pytest

@pytest.fixture
def given_a_batch_and_order_line_item():

    def _given_a_batch_and_order_line_item(sku, batch_qty, line_qty):
        return(
            LineItem("order_id", sku=sku, quantity=line_qty),
            Batch("batch_id", sku=sku, quantity=batch_qty, eta=date.today())
        )
    return _given_a_batch_and_order_line_item


# allocate order lines to batches
def test_allocate_order_lines_to_batches(given_a_batch_and_order_line_item):
    # Setup
    # get line items and batch
    order_line_item, batch = given_a_batch_and_order_line_item(sku="SMALL-TABLE",
                                                               batch_qty=20,
                                                               line_qty=2)
    # Excercise
    # Allocate line itens
    batch.allocate(order_line_item)
    # Verify
    assert batch.available_quantity == 18


# can or can´t allocate to a batch with diferents available quantity
@pytest.mark.parametrize("batch_lin_qty, expected",
                    [
                        ([2, 1],True),
                        ([1, 2], False),
                        ([1, 1], True)
                    ]
                         )
def test_allocate_different_quantities(given_a_batch_and_order_line_item, batch_lin_qty, expected):
    # Setup
    # get line items and batch
    order_line_item, batch = given_a_batch_and_order_line_item(sku="SMALL-TABLE",
                                                               batch_qty=batch_lin_qty[0],
                                                               line_qty=batch_lin_qty[1])
    assert batch.can_allocate(order_line_item) == expected


def test_cant_allocate_if_sku_not_match():
    # setup
    order_line_item = LineItem("order_001", sku="SMALL-TABLE", quantity=3)
    batch = Batch("batch_001", sku="BIG_TABLE", quantity=2, eta=date.today())
    # Excercise
    assert not batch.can_allocate(order_line_item)


def test_can_only_deallocate_allocated_lines(given_a_batch_and_order_line_item):
    order_line_item, batch = given_a_batch_and_order_line_item(sku="SMALL-TABLE",
                                                               batch_qty=20,
                                                               line_qty=2)
    batch.deallocate(order_line_item)
    assert batch.available_quantity == 20


# allocate is idempotent
def test_cant_allocate_the_same_line_twice(given_a_batch_and_order_line_item):
    # Setup
    # get line items and batch
    order_line_item, batch = given_a_batch_and_order_line_item(sku="SMALL-TABLE",
                                                               batch_qty=20,
                                                               line_qty=2)
    # Excercise
    # Allocate line itens
    batch.allocate(order_line_item)
    batch.allocate(order_line_item)
    # Verify
    assert batch.available_quantity == 18


# Allocate first in stock against shipments
def test_prefers_current_stock_batches_to_shipments():
    tomorrow = timedelta(days=1)
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=date.today()+tomorrow)
    order_line = LineItem("oref", "RETRO-CLOCK", 10)

    allocate(order_line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=date.today())
    medium = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=date.today()+timedelta(days=1))
    latest = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=date.today()+timedelta(days=2))
    order_line = LineItem("oref", "RETRO-CLOCK", 10)

    allocate(order_line,[earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100

def test_returns_allocated_batch_ref():
    tomorrow = timedelta(days=1)
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=date.today()+tomorrow)
    order_line = LineItem("oref", "RETRO-CLOCK", 10)

    allocations = allocate(order_line, [in_stock_batch, shipment_batch])

    assert allocations == in_stock_batch.reference
