from datetime import datetime
from uuid import UUID
from apps.categories.entity import Category
from tests.utils import parse_iso_datetime

def assert_has_valid_timestamps(body: dict) -> None:
        assert "created_at" in body
        assert "updated_at" in body
        datetime_created_at = parse_iso_datetime(body["created_at"])
        assert isinstance(datetime_created_at, datetime)
        assert "updated_at" in body
        datetime_updated_at = parse_iso_datetime(body["updated_at"])
        assert isinstance(datetime_updated_at, datetime)


def assert_has_valid_id(body: dict) -> None:
        assert "id" in body
        assert isinstance(UUID(body["id"]), UUID)
