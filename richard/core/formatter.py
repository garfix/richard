def format_value(value: any, indent: str = "\n") -> str:
    """
    Formats nested lists, tuples and strings
    """
    if isinstance(value, tuple):
        text = indent + "("
        sep = ""
        for element in value:
            text += sep + format_value(element, indent + "    ")
            sep = ", "
        text += ")"
    elif isinstance(value, list):
        text = indent + "["
        for element in value:
            text += format_value(element, indent + "    ")
        text += indent + "]"
    elif isinstance(value, str):
        text = "'" + value + "'"
    else:
        text = str(value)
    return text
