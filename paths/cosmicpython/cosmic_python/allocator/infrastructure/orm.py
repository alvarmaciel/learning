from sqlalchemy import MetaData, Table, Integer, String, Column, Date, ForeignKey
from sqlalchemy.orm import relationship, registry
from allocator.domain.models import LineItem, Batch

mapper = registry()
metadata = MetaData()

line_items = Table(
    'line_items',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('order_id', String(255)),
    Column('sku', String(255)),
    Column('quantity', Integer, nullable=False ),
)

batches = Table(
    'batches',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reference', String(255)),
    Column('sku', String(255)),
    Column('_purchased_quantity', Integer, nullable=False),
    Column('eta', Date)
)

allocations = Table(
    'allocations',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('line_items_id', ForeignKey("line_items.id")),
    Column('batches_id', ForeignKey("batches.id"))
)


def start_mappers():

    lines_mapper = mapper.map_imperatively(LineItem, line_items)

    mapper.map_imperatively(
        Batch,
        batches,
        properties={
            "_allocations": relationship(
                LineItem,
                #backref="batch",
                #lazy="select",
                secondary=allocations,
                collection_class=set)
        }
    )
