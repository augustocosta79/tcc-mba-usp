from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"
