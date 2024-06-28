from .base_schema import BaseSchema
from .brand_schema import BrandId, BrandUpdIn, BrandNewIn, BrandName, BrandNewOut, BrandUpdOut, BrandDelete
from .margin_schema import Margin
from .catalog_schema import (CatalogIn,
                             CatalogOutById,
                             CatalogOutByNumber,
                             CatalogUpdIn,
                             CatalogUpdOut,
                             CatalogInOut,
                             CatalogDelete)
from .auth_schema import Tokens, GetMe
from .employee_schema import NewEmployee, EmployeeOut, EmployeeUpdIn, EmployeeUpdOut, NewEmployeeOut
from .role_schema import RoleOut
from .shop_schema import ShopUpd, ShopIn, ShopOut, ShopDelete
from .supplier_schema import OrgAttr, SupplierIn, SupplierOut, SupplierListOut, SupplierUpdate
from .new_arrival_schema import (
    NewArrivalIn,
    NewArrivalOut,
    ArrivalNewOut,
    ArrivalDetailNewIn,
    ArrivalDetailNewOut,
    NewArrivalDetailGetList,
    NewArrivalUpdateIn,
    NewArrivalUpdateOut,
    NewArrivalDetailUpdateIn,
    NewArrivalDetailUpdateOut,
    NewArrivalDeleteOut,
    NewArrivalDetailDeleteOut
)
from .actual_product_schema import (
    ActualProductOutByPartId,
    ActualProductOutById,
    ActualProductUpdateIn,
    ActualProductUpdateOut
)
from .client_schema import PhysicalClientIn, PhysicalClientOut, JuridicalClientIn, JuridicalClientOut
