-- Creates a trigge that decreases the quantity of an item after adding a new order
-- Quantity in the table items can be negative

DELIMETER $$ ;
CREATE TRIGGER decrease_the_quantity AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - 1
    WHERE id = NEW.item_id;
END;
DELIMETER ;