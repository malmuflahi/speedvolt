class InvoiceService:
    @staticmethod
    def format_order_id(order_id):
        return f"SV-{order_id:06d}"