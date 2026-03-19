def format_price(value):
    return f"${value:.2f}"


def isNumeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False