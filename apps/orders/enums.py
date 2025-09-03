from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

    @property
    def previous(self):
        previous_map = {
            "approved": "pending",
            "shipped": "approved",
            "delivered": "shipped",
            "canceled": "pending",
            "pending": None,
        }
        prev = previous_map[self.value]
        return OrderStatus(prev) if prev else None
    

class OrderItemOperation(str, Enum):
    INCREASE = "increase"
    DECREASE =  "decrease"
