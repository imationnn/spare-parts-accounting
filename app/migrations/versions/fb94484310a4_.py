"""empty message

Revision ID: fb94484310a4
Revises: 
Create Date: 2024-05-28 17:52:53.193424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb94484310a4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('brands',
    sa.Column('brand_name', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('catalog_cars',
    sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('margin_categories',
    sa.Column('margin_value', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('org_attrs',
    sa.Column('inn', sa.String(), nullable=True),
        sa.Column('ogrn', sa.String(), nullable=True),
        sa.Column('kpp', sa.String(), nullable=True),
        sa.Column('okved', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('bank_name', sa.String(), nullable=True),
        sa.Column('bik', sa.String(), nullable=True),
        sa.Column('r_s', sa.String(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_methods',
    sa.Column('eng_name', sa.String(), nullable=False),
        sa.Column('rus_name', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('physical_clients',
    sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('patronymic', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('sale', sa.Integer(), server_default='0', nullable=False),
        sa.Column('sale_card', sa.String(), nullable=True),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('is_black_list', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sale_card')
    )
    op.create_table('roles',
    sa.Column('eng_name', sa.String(), nullable=False),
        sa.Column('rus_name', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shops',
    sa.Column('short_name', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='True', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ip_address'),
        sa.UniqueConstraint('short_name')
    )
    op.create_table('status_movements',
    sa.Column('eng_name', sa.String(), nullable=False),
        sa.Column('rus_name', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status_orders',
    sa.Column('eng_name', sa.String(), nullable=False),
        sa.Column('rus_name', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status_receipts',
    sa.Column('eng_name', sa.String(), nullable=False),
        sa.Column('rus_name', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('catalog_parts',
    sa.Column('number', sa.String(), nullable=False),
        sa.Column('brand_id', sa.Integer(), nullable=False),
        sa.Column('desc_eng', sa.String(), nullable=True),
        sa.Column('desc_rus', sa.String(), nullable=False),
        sa.Column('margin_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('search_id', sa.String(), nullable=False),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
        sa.ForeignKeyConstraint(['margin_id'], ['margin_categories.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('number', 'brand_id', name='catalog_parts_unique')
    )
    op.create_table('client_cars',
    sa.Column('car_id', sa.Integer(), nullable=False),
        sa.Column('vin_code', sa.String(), nullable=True),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('physical_client_id', sa.Integer(), nullable=True),
        sa.Column('juridical_client_id', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['car_id'], ['catalog_cars.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employees',
    sa.Column('login', sa.String(), nullable=False),
        sa.Column('password', sa.LargeBinary(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='True', nullable=False),
        sa.Column('role_id', sa.Integer(), server_default='3', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login')
    )
    op.create_table('incoming_movements',
    sa.Column('from_shop_id', sa.Integer(), nullable=False),
        sa.Column('to_shop_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Integer(), server_default='5', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('arrived_at', sa.DateTime(), nullable=True),
        sa.Column('created_employee_id', sa.Integer(), nullable=False),
        sa.Column('accepted_employee_id', sa.Integer(), nullable=True),
        sa.Column('total_price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['from_shop_id'], ['shops.id'], ),
        sa.ForeignKeyConstraint(['status'], ['status_movements.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('juridical_clients',
    sa.Column('org_name', sa.String(), nullable=False),
        sa.Column('sale', sa.Integer(), server_default='0', nullable=False),
        sa.Column('sale_card', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('is_black_list', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('org_attr_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['org_attr_id'], ['org_attrs.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sale_card')
    )
    op.create_table('outgoing_movements',
    sa.Column('from_shop_id', sa.Integer(), nullable=False),
        sa.Column('to_shop_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Integer(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('created_employee_id', sa.Integer(), nullable=False),
        sa.Column('total_price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['status'], ['status_movements.id'], ),
        sa.ForeignKeyConstraint(['to_shop_id'], ['shops.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('physical_sale_receipts',
    sa.Column('client_id', sa.Integer(), nullable=True),
        sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('total_price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('payment_method_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('client_car_id', sa.Integer(), nullable=True),
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['physical_clients.id'], ),
        sa.ForeignKeyConstraint(['payment_method_id'], ['payment_methods.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status_receipts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('suppliers',
    sa.Column('org_name', sa.String(), nullable=False),
        sa.Column('org_attr_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['org_attr_id'], ['org_attrs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('juridical_orders',
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('prepayment', sa.Numeric(precision=20, scale=2), server_default='0', nullable=False),
        sa.Column('total_price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('payment_method_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('is_print', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('is_notify', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('client_car_id', sa.Integer(), nullable=True),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['client_car_id'], ['client_cars.id'], ),
        sa.ForeignKeyConstraint(['client_id'], ['juridical_clients.id'], ),
        sa.ForeignKeyConstraint(['payment_method_id'], ['payment_methods.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status_orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('juridical_sale_receipts',
    sa.Column('client_id', sa.Integer(), nullable=True),
        sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('total_price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('payment_method_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('client_car_id', sa.Integer(), nullable=True),
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['juridical_clients.id'], ),
        sa.ForeignKeyConstraint(['payment_method_id'], ['payment_methods.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status_receipts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('new_arrivals',
    sa.Column('invoice_number', sa.String(), nullable=False),
        sa.Column('invoice_date', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=False),
        sa.Column('total_price', sa.Numeric(precision=20, scale=2), server_default='0', nullable=False),
        sa.Column('is_transferred', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('invoice_number', 'supplier_id', name='arrival_unique')
    )
    op.create_table('physical_orders',
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('prepayment', sa.Numeric(precision=20, scale=2), server_default='0', nullable=False),
        sa.Column('total_price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('payment_method_id', sa.Integer(), server_default='1', nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('is_print', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('is_notify', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('client_car_id', sa.Integer(), nullable=True),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['client_car_id'], ['client_cars.id'], ),
        sa.ForeignKeyConstraint(['client_id'], ['physical_clients.id'], ),
        sa.ForeignKeyConstraint(['payment_method_id'], ['payment_methods.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status_orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('actual_products',
    sa.Column('part_id', sa.Integer(), nullable=False),
        sa.Column('arrived', sa.Integer(), nullable=False),
        sa.Column('released', sa.Integer(), server_default='0', nullable=False),
        sa.Column('rest', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('movement_id', sa.Integer(), nullable=True),
        sa.Column('reserve', sa.Integer(), server_default='0', nullable=False),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('arrive_id', sa.Integer(), nullable=False),
        sa.Column('arrived_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('safety_reserve', sa.Integer(), nullable=True),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['arrive_id'], ['new_arrivals.id'], ),
        sa.ForeignKeyConstraint(['part_id'], ['catalog_parts.id'], ),
        sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('juridical_order_details',
    sa.Column('part_id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), server_default='6', nullable=False),
        sa.Column('qty_available', sa.Integer(), server_default='0', nullable=False),
        sa.Column('qty_needed', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('sale', sa.Integer(), server_default='0', nullable=False),
        sa.Column('prepayment_part', sa.Numeric(precision=20, scale=2), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('change_time', sa.DateTime(), nullable=True),
        sa.Column('change_employee_id', sa.Integer(), nullable=True),
        sa.Column('sales_receipt_id', sa.Integer(), nullable=True),
        sa.Column('sale_id', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['juridical_orders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['part_id'], ['catalog_parts.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status_orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('new_arrival_details',
    sa.Column('part_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('price_in', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('amount', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('currency', sa.String(), server_default='RUB', nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('ccd', sa.String(), nullable=True),
        sa.Column('arrive_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['arrive_id'], ['new_arrivals.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.ForeignKeyConstraint(['part_id'], ['catalog_parts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('physical_order_details',
    sa.Column('part_id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), server_default='6', nullable=False),
        sa.Column('qty_available', sa.Integer(), server_default='0', nullable=False),
        sa.Column('qty_needed', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('sale', sa.Integer(), server_default='0', nullable=False),
        sa.Column('prepayment_part', sa.Numeric(precision=20, scale=2), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('change_time', sa.DateTime(), nullable=True),
        sa.Column('change_employee_id', sa.Integer(), nullable=True),
        sa.Column('sales_receipt_id', sa.Integer(), nullable=True),
        sa.Column('sale_id', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['physical_orders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['part_id'], ['catalog_parts.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status_orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('incoming_movement_details',
    sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Integer(), server_default='5', nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('move_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['move_id'], ['incoming_movements.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['actual_products.id'], ),
        sa.ForeignKeyConstraint(['status'], ['status_movements.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('juridical_sale_receipt_details',
    sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('qty_available', sa.Integer(), nullable=False),
        sa.Column('qty_needed', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), server_default='4', nullable=False),
        sa.Column('price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('amount', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('sale', sa.Integer(), server_default='0', nullable=False),
        sa.Column('prepayment_part', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('paid_time', sa.DateTime(), nullable=True),
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('sale_id', sa.Integer(), nullable=False),
        sa.Column('order_det_id', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['actual_products.id'], ),
        sa.ForeignKeyConstraint(['sale_id'], ['juridical_sale_receipts.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status_receipts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('outgoing_movement_details',
    sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Integer(), server_default='6', nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('move_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['move_id'], ['outgoing_movements.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['actual_products.id'], ),
        sa.ForeignKeyConstraint(['status'], ['status_movements.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('physical_sale_receipt_details',
    sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('qty_available', sa.Integer(), nullable=False),
        sa.Column('qty_needed', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), server_default='4', nullable=False),
        sa.Column('price', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('amount', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('sale', sa.Integer(), server_default='0', nullable=False),
        sa.Column('prepayment_part', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('paid_time', sa.DateTime(), nullable=True),
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('sale_id', sa.Integer(), nullable=False),
        sa.Column('order_det_id', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['actual_products.id'], ),
        sa.ForeignKeyConstraint(['sale_id'], ['physical_sale_receipts.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status_receipts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('physical_sale_receipt_details')
    op.drop_table('outgoing_movement_details')
    op.drop_table('juridical_sale_receipt_details')
    op.drop_table('incoming_movement_details')
    op.drop_table('physical_order_details')
    op.drop_table('new_arrival_details')
    op.drop_table('juridical_order_details')
    op.drop_table('actual_products')
    op.drop_table('physical_orders')
    op.drop_table('new_arrivals')
    op.drop_table('juridical_sale_receipts')
    op.drop_table('juridical_orders')
    op.drop_table('suppliers')
    op.drop_table('physical_sale_receipts')
    op.drop_table('outgoing_movements')
    op.drop_table('juridical_clients')
    op.drop_table('incoming_movements')
    op.drop_table('employees')
    op.drop_table('client_cars')
    op.drop_table('catalog_parts')
    op.drop_table('status_receipts')
    op.drop_table('status_orders')
    op.drop_table('status_movements')
    op.drop_table('shops')
    op.drop_table('roles')
    op.drop_table('physical_clients')
    op.drop_table('payment_methods')
    op.drop_table('org_attrs')
    op.drop_table('margin_categories')
    op.drop_table('catalog_cars')
    op.drop_table('brands')
