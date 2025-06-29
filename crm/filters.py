import django_filters
from crm.models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    """
    Filter class for the Customer model.
    This class defines the filters available for querying customers.
    """

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    phone_pattern = django_filters.CharFilter(field_name="phone", method="filter_phone")
    created_at__gte = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at__lte = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    def filter_phone(self, queryset, name, value):
        """
        Custom filter method for phone numbers.
        This method allows filtering by phone number that starts with +1.
        """
        return queryset.filter(phone__startswith=value)

    order_by = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("email", "email"),
            ("created_at", "created_at"),
        )
    )

    class Meta:
        """Meta class for the CustomerFilter."""

        model = Customer
        fields = [
            "name",
            "email",
            "phone_pattern",
            "created_at__gte",
            "created_at__lte",
        ]


class ProductFilter(django_filters.FilterSet):
    """Filter class for the Product model."""

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    stock__gte = django_filters.NumberFilter(field_name="stock", lookup_expr="gte")
    stock__lte = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")
    stock_lt_10 = django_filters.NumberFilter(
        method="filter_stock_lt_10", label="Stock < 10"
    )

    def filter_stock_lt_10(self, queryset, name, value):
        """Custom filter method for stock less than 10."""
        return queryset.filter(stock__lt=10)

    order_by = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("price", "price"),
            ("stock", "stock"),
        )
    )

    class Meta:
        """Meta class for the ProductFilter."""

        model = Product
        fields = [
            "name",
            "price__gte",
            "price__lte",
            "stock__gte",
            "stock__lte",
            "stock_lt_10",
        ]


class OrderFilter(django_filters.FilterSet):
    """Filter class for the Order model."""

    customer_name = django_filters.CharFilter(
        field_name="customer__name", lookup_expr="icontains"
    )
    product_name = django_filters.CharFilter(
        method="filter_product_name",
        label="Product Name",
    )
    total_amount__gte = django_filters.NumberFilter(
        field_name="total_amount", lookup_expr="gte"
    )
    total_amount__lte = django_filters.NumberFilter(
        field_name="total_amount", lookup_expr="lte"
    )
    order_date__gte = django_filters.DateTimeFilter(
        field_name="order_date", lookup_expr="gte"
    )
    order_date__lte = django_filters.DateTimeFilter(
        field_name="order_date", lookup_expr="lte"
    )
    product_id = django_filters.NumberFilter(
        method="filter_product_id",
        label="Product ID",
    )

    def filter_product_name(self, queryset, name, value):
        """
        Custom filter method for product names in orders.
        This method allows filtering orders by product names.
        """
        return queryset.filter(products__name__icontains=value)

    def filter_product_id(self, queryset, name, value):
        """
        Custom filter method for product IDs in orders.
        This method allows filtering orders by product IDs.
        """
        return queryset.filter(products__id=value)

    order_by = django_filters.OrderingFilter(
        fields=(
            ("order_date", "order_date"),
            ("total_amount", "total_amount"),
        )
    )

    class Meta:
        """Meta class for the OrderFilter."""

        model = Order
        fields = [
            "customer_name",
            "product_name",
            "product_id",
            "total_amount__gte",
            "total_amount__lte",
            "order_date__gte",
            "order_date__lte",
        ]
