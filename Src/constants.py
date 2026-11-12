# constants.py
"""Canonical string values used across CRUD and menus.
Prevents typos like 'delivred' vs 'delivered'."""

# Order statuses
ORDER_PENDING = "pending"
ORDER_CONFIRMED = "confirmed"
ORDER_OUT_FOR_DELIVERY = "out_for_delivery"
ORDER_DELIVERED = "delivered"
ORDER_CANCELLED = "cancelled"

ORDER_STATUSES = (
    ORDER_PENDING,
    ORDER_CONFIRMED,
    ORDER_OUT_FOR_DELIVERY,
    ORDER_DELIVERED,
    ORDER_CANCELLED,
)

# Route statuses
ROUTE_PLANNED = "planned"
ROUTE_IN_PROGRESS = "in_progress"
ROUTE_COMPLETED = "completed"
ROUTE_CANCELLED = "cancelled"

ROUTE_STATUSES = (
    ROUTE_PLANNED,
    ROUTE_IN_PROGRESS,
    ROUTE_COMPLETED,
    ROUTE_CANCELLED,
)

# Billing statuses
BILLING_UNPAID = "unpaid"
BILLING_PAID = "paid"
BILLING_OVERDUE = "overdue"
BILLING_CANCELLED = "cancelled"

BILLING_STATUSES = (
    BILLING_UNPAID,
    BILLING_PAID,
    BILLING_OVERDUE,
    BILLING_CANCELLED,
)

# User roles
ROLE_ADMIN = "admin"
ROLE_CLERK = "clerk"
ROLE_DRIVER = "driver"

USER_ROLES = (ROLE_ADMIN, ROLE_CLERK, ROLE_DRIVER)