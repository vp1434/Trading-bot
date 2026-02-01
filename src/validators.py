import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class OrderValidator:
    """Validates order parameters before submission."""
    
    VALID_SIDES = ['BUY', 'SELL']
    VALID_ORDER_TYPES = ['MARKET', 'LIMIT']
    
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """Validate trading symbol format."""
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol must be a non-empty string")
        
        symbol = symbol.upper().strip()
        
        if not symbol.endswith('USDT'):
            logger.warning(f"Symbol {symbol} doesn't end with USDT - may not be valid for USDT-M futures")
        
        return symbol
    
    @staticmethod
    def validate_side(side: str) -> str:
        """Validate order side."""
        if not side or not isinstance(side, str):
            raise ValidationError("Side must be a non-empty string")
        
        side = side.upper().strip()
        
        if side not in OrderValidator.VALID_SIDES:
            raise ValidationError(f"Side must be one of {OrderValidator.VALID_SIDES}, got: {side}")
        
        return side
    
    @staticmethod
    def validate_order_type(order_type: str) -> str:
        """Validate order type."""
        if not order_type or not isinstance(order_type, str):
            raise ValidationError("Order type must be a non-empty string")
        
        order_type = order_type.upper().strip()
        
        if order_type not in OrderValidator.VALID_ORDER_TYPES:
            raise ValidationError(f"Order type must be one of {OrderValidator.VALID_ORDER_TYPES}, got: {order_type}")
        
        return order_type
    
    @staticmethod
    def validate_quantity(quantity: float) -> float:
        """Validate order quantity."""
        try:
            quantity = float(quantity)
        except (ValueError, TypeError):
            raise ValidationError(f"Quantity must be a valid number, got: {quantity}")
        
        if quantity <= 0:
            raise ValidationError(f"Quantity must be greater than 0, got: {quantity}")
        
        return quantity
    
    @staticmethod
    def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
        """Validate order price."""
        if order_type == 'LIMIT':
            if price is None:
                raise ValidationError("Price is required for LIMIT orders")
            
            try:
                price = float(price)
            except (ValueError, TypeError):
                raise ValidationError(f"Price must be a valid number, got: {price}")
            
            if price <= 0:
                raise ValidationError(f"Price must be greater than 0, got: {price}")
        
        return price
    
    @classmethod
    def validate_order(cls, symbol: str, side: str, order_type: str, 
                      quantity: float, price: Optional[float] = None) -> dict:
        """Validate all order parameters and return cleaned values."""
        logger.info("Validating order parameters...")
        
        validated = {
            'symbol': cls.validate_symbol(symbol),
            'side': cls.validate_side(side),
            'order_type': cls.validate_order_type(order_type),
            'quantity': cls.validate_quantity(quantity),
            'price': cls.validate_price(price, order_type)
        }
        
        logger.info("Order parameters validated successfully")
        return validated
