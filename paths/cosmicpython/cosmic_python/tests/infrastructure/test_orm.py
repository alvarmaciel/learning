from allocator.domain.models import LineItem, Batch
from sqlalchemy import text

def test_line_item_mapper_can_load_lines(session):

    insert = text(
        "INSERT INTO line_items (order_id, sku, quantity) VALUES "
        "('order1', 'RED-CHAIR', 10), "
        "('order2', 'BLUE-CHAIR', 5), "
        "('order3', 'GREEN-TABLE', 3)"
    )
    session.execute(insert)

    expected = [
        LineItem('order1', 'RED-CHAIR', 10),
        LineItem('order2', 'BLUE-CHAIR', 5),
        LineItem('order3', 'GREEN-TABLE', 3),
    ]
    assert session.query(LineItem).all() == expected

def test_line_item_mapper_can_save_lines(session):

    new_line = LineItem('order1', 'RED-CHAIR', 10)
    session.add(new_line)
    session.commit()
    query = text(
        "SELECT order_id, sku, quantity FROM line_items"
    )
    rows = list(session.execute(query))
    assert rows == [('order1', 'RED-CHAIR', 10)]

def test_batch_mapper_can_load_batches(session):

    insert = text(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES "
        "('batch1', 'RED-CHAIR', 100, null), "
        "('batch2', 'BLUE-CHAIR', 100, '2011-04-11'), "
        "('batch3', 'GREEN-TABLE', 100, null)"
    )
    session.execute(insert)

    expected = [
        Batch('batch1', 'RED-CHAIR', 100, None),
        Batch('batch2', 'BLUE-CHAIR', 100, '2011-04-11'),
        Batch('batch3', 'GREEN-TABLE', 100, None),
    ]
    assert session.query(Batch).all() == expected

def test_batch_mapper_can_save_batches(session):
    new_batch = Batch('batch1', 'RED-CHAIR', 100, None)
    session.add(new_batch)
    session.commit()
    query = text(
        "SELECT reference, sku, _purchased_quantity, eta FROM batches"
    )
    rows = list(session.execute(query))
    assert rows == [('batch1', 'RED-CHAIR', 100, None)]
