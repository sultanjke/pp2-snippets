def handle_order_status(status):
    match status:
        case "pending":
            print("Order is pending")
        case "shipped":
            print("Order is shipped")
        case "delivered":
            print("Order is delivered")
        case _:
            print("Unknown status")

# Usage
handle_order_status("shipped")  # Output: "Order is shipped"