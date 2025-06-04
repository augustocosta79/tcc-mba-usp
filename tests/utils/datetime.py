from datetime import datetime, timezone

def parse_iso_datetime(date_str: str) -> datetime:
    """
    Converte string no formato ISO 8601 com Z (UTC) para datetime com timezone UTC.
    """
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
