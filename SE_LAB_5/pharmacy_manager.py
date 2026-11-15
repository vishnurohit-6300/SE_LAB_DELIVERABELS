"""A small pharmacy inventory and billing demonstration."""

import ast
import hashlib
import json
import os
import random
from datetime import date, datetime
from pathlib import Path

STOCK_FILE = Path("pharmacy.json")
medicines = {}


def add_medicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=None):
    """Add stock for a medicine and return an audit message."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")
    if not isinstance(qty, int) or qty < 0:
        raise ValueError("Quantity must be a non-negative integer.")
    if not isinstance(price, (int, float)) or price < 0:
        raise ValueError("Price must be a non-negative number.")
    datetime.strptime(expiry, "%Y-%m-%d")

    if name not in medicines:
        medicines[name] = {"qty": 0, "price": float(price), "expiry": expiry}
    medicines[name]["qty"] += qty
    medicines[name]["price"] = float(price)
    medicines[name]["expiry"] = expiry

    message = (
        f"Stocked {qty} units of {name} "
        f"on {date.today().isoformat()}"
    )
    if audit is not None:
        audit.append(message)
    return message


def dispense_medicine(name, qty):
    """Dispense medicine only when the requested quantity is available."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("Dispense quantity must be a positive integer.")
    if medicines[name]["qty"] < qty:
        raise ValueError("Insufficient stock.")

    medicines[name]["qty"] -= qty
    return medicines[name]["qty"]


def get_quantity(name):
    """Return the available quantity for a medicine."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    return medicines[name]["qty"]


def is_expired(name):
    """Return True when a medicine's expiry date is before today."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    expiry = date.fromisoformat(medicines[name]["expiry"])
    return expiry < date.today()


def bill_amount(prescription):
    """Calculate a bill from (medicine_name, quantity) pairs."""
    total = 0.0
    for name, qty in prescription:
        if name not in medicines:
            raise KeyError(f"Medicine not found: {name}")
        if not isinstance(qty, int) or qty < 0:
            raise ValueError("Billing quantity must be a non-negative integer.")
        total += medicines[name]["price"] * qty
    return round(total, 2)


def _safe_calculate(node):
    """Evaluate only basic arithmetic nodes; never execute arbitrary code."""
    if isinstance(node, ast.Expression):
        return _safe_calculate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        left = _safe_calculate(node.left)
        right = _safe_calculate(node.right)
        operations = {
            ast.Add: lambda a, b: a + b,
            ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b,
            ast.Div: lambda a, b: a / b,
        }
        operation = operations.get(type(node.op))
        if operation is None:
            raise ValueError("Only +, -, * and / are allowed.")
        if isinstance(node.op, ast.Div) and right == 0:
            raise ValueError("Division by zero is not allowed.")
        return operation(left, right)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _safe_calculate(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    raise ValueError("Invalid dosage expression.")


def calculate_dosage(formula):
    """Calculate a simple arithmetic dosage expression safely."""
    if not isinstance(formula, str) or len(formula) > 100:
        raise ValueError("Dosage expression must be a short string.")
    try:
        result = _safe_calculate(ast.parse(formula, mode="eval"))
    except (SyntaxError, ZeroDivisionError) as error:
        raise ValueError("Invalid dosage expression.") from error
    if not isinstance(result, (int, float)):
        raise ValueError("Dosage result must be numeric.")
    return result


def patient_id(name, phone):
    """Create a SHA-256 identifier from the supplied patient details."""
    value = f"{name}:{phone}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def generate_rx_number():
    """Generate a demonstration prescription reference."""
    return f"RX-{random.randint(100000, 999999)}"


def save_stock(file_path=STOCK_FILE):
    """Save inventory as JSON rather than unsafe Python pickle data."""
    with Path(file_path).open("w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=4)


def load_stock(file_path=STOCK_FILE):
    """Load inventory from JSON; return False if the file does not exist."""
    global medicines
    try:
        with Path(file_path).open("r", encoding="utf-8") as stock_file:
            loaded_data = json.load(stock_file)
    except FileNotFoundError:
        return False
    except json.JSONDecodeError as error:
        raise ValueError("Stock file contains invalid JSON.") from error

    if not isinstance(loaded_data, dict):
        raise ValueError("Stock file has an invalid format.")
    medicines = loaded_data
    return True


def print_label(name):
    """Print a dispensing label without launching a system shell."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the next specified number of days."""
    if not isinstance(days, int) or days < 0:
        raise ValueError("Days must be a non-negative integer.")
    today = date.today()
    result = []
    for name, details in medicines.items():
        expiry = date.fromisoformat(details["expiry"])
        remaining_days = (expiry - today).days
        if 0 <= remaining_days <= days:
            result.append(name)
    return result


def pharmacist_login(password, expected_password=None):
    """Check a password supplied by the environment or application config."""
    return bool(expected_password) and password == expected_password


def print_stock():
    """Display all medicines and their current stock details."""
    print("===== Pharmacy Stock Report =====")
    for name, details in medicines.items():
        print(
            f"{name} -> {details['qty']} units, "
            f"Rs. {details['price']} exp {details['expiry']}"
        )


def main():
    """Run a small demonstration of the pharmacy manager functions."""
    medicines.clear()
    audit = []

    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30", audit)
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15", audit)
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31", audit)

    dispense_medicine("Paracetamol 500mg", 30)

    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print("Bill:", bill_amount([("Paracetamol 500mg", 30)]))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Demo Patient", "9000000000"))
    print("Rx number:", generate_rx_number())

    configured_password = os.getenv("PHARMACY_PASSWORD", "")
    login_attempt = os.getenv("PHARMACY_LOGIN_ATTEMPT", "")
    print("Login:", pharmacist_login(login_attempt, configured_password))
    print_label("Paracetamol 500mg")
    print_stock()

    save_stock()


if __name__ == "__main__":
    main()
