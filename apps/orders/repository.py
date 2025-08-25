from uuid import UUID
from apps.orders.repository_interface import OrderRepositoryInterface
from apps.orders.entity import Order, OrderItem
from apps.orders.models import OrderModel, OrderItemModel
from apps.shared.value_objects import Price
from apps.products.product_entity import Product


class OrderRepository(OrderRepositoryInterface):
    def save(self, order: Order) -> Order:
        order_data = OrderModel.objects.create(
            id=order.id,
            user_id=order.user_id,
            address_id=order.address_id,
            status=order.status,
            total_amount=order.total_amount.value,
        )

        items_model = [
            OrderItemModel.objects.create(
                order=order_data,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price.value,
            )
            for item in order.items
        ]

        items = [
            OrderItem(item.product_id, item.quantity, Price(item.price), item.id)
            for item in items_model
        ]

        return Order(
            order_data.user_id,
            order_data.address_id,
            items,
            order_data.status,
            order_data.id,
        )
    
    def get_order_by_id(self, order_id: UUID):
        if not (order_data:=OrderModel.objects.filter(id=order_id).first()):
            return None
        
        items_data = order_data.items.all()

        items = [
            OrderItem(item.product_id, item.quantity, Price(item.price), item.id)
            for item in items_data
        ]

        return Order(
            order_data.user_id,
            order_data.address_id,
            items,
            order_data.status,
            order_data.id,
        )

        
