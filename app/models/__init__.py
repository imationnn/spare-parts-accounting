from .base import Base, created_at, int_def0, def_false
from .actual_product import ActualProduct, Shop
from .car import ClientCar, CatalogCar
from .catalog import CatalogPart, MarginCategory, Brand, MarginCategories
from .contractor import Supplier, OrgAttr, PhysicalClient, JuridicalClient
from .employee import Employee, Role, Roles
from .movement import (IncomingMovement, OutgoingMovement, IncomingMovementDetail, OutgoingMovementDetail,
                       StatusMovement, StatusMovements)
from .new_arrival import NewArrival, NewArrivalDetail
from .order import PhysicalOrder, JuridicalOrder, StatusOrder, StatusOrders, PhysicalOrderDetail, JuridicalOrderDetail
from .payment_method import PaymentMethods, PaymentMethod
from .sale_receipt import (PhysicalSaleReceipt, JuridicalSaleReceipt, PhysicalSaleReceiptDetail,
                           JuridicalSaleReceiptDetail, StatusReceipts, StatusReceipt)
