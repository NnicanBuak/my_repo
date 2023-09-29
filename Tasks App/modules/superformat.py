def float(number: float, precision=2) -> str:
    number_parts: list[str] = str(number).split('.')
    if len(number_parts) == 2:
        return number_parts[0] + '.' + number_parts[1][:-(len(number_parts[1].lstrip('0'))-precision) if len(number_parts[1].lstrip('0'))-precision > 0 else 0] if number_parts[1].lstrip('0') else number_parts[0]
    else:
        return number_parts[0]