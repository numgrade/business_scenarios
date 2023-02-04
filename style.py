"""Styling for pandas DataFrame display."""


def style_negative(v, props='color:red;'):
    """Return CSS color if value is negative."""
    return props if v < 0 else None