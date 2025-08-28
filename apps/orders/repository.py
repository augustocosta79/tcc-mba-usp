from uuid import UUID
from apps.orders.repository_interface import OrderRepositoryInterface
from apps.orders.entity import Order, OrderItem
from apps.orders.models import OrderModel, OrderItemModel
from apps.shared.value_objects import Price
from apps.products.product_entity import Product
from apps.orders.enums import OrderStatus


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
                id=item.id,
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
            OrderStatus(order_data.status),
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
            OrderStatus(order_data.status),
            order_data.id,
        )
    
    def list_orders_by_user_id(self, user_id: UUID):
        orders_data = OrderModel.objects.filter(user_id=user_id)
        return [
            Order(
                order_data.user_id,
                order_data.address_id,
                [
                    OrderItem(item.product_id, item.quantity, Price(item.price), item.id)
                    for item in order_data.items.all()
                ],
                OrderStatus(order_data.status),
                order_data.id,
            )
            for order_data in orders_data
        ]
    
    def set_status(self, order_id: UUID, new_status: OrderStatus) -> None:
        if not (order_data:=OrderModel.objects.filter(id=order_id).first()):
            return None
        order_data.status = new_status
        order_data.save()

        items_data = order_data.items.all()
        items = [
            OrderItem(item.product_id, item.quantity, Price(item.price), item.id)
            for item in items_data
        ]

        return Order(
            order_data.user_id,
            order_data.address_id,
            items,
            OrderStatus(order_data.status),
            order_data.id,
        )

    def delete_order_item(self, item_id: UUID) -> None:
        OrderItemModel.objects.filter(id=item_id).delete()
   

    def update_order(self, order: Order) -> Order:
        order_model = OrderModel.objects.filter(id=order.id).first()
        if not order_model:
            return None

        order_model.status = order.status.value
        order_model.address_id = order.address_id
        order_model.total_amount = order.total_amount.value
        order_model.save()

        order_model.items.all().delete()

        items_model = [
            OrderItemModel.objects.create(
                id=item.id,
                order=order_model,
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
            order_model.user_id,
            order_model.address_id,
            items,
            OrderStatus(order_model.status),
            order_model.id,
        )
