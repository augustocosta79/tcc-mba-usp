from apps.shared.decorators.require_active_user import  require_active_user
from types import SimpleNamespace
from ninja.errors import HttpError
from uuid import uuid4
from unittest.mock import patch

class TestRequireActiveUser:
    @patch("apps.shared.decorators.require_active_user.UserModel.objects.get")
    def test_should_allow_active_user(self, mock_get):
        user_id = uuid4()
        mock_get.return_value = SimpleNamespace(is_active=True)

        @require_active_user
        def dummy_handler(request):
            return "OK"

        request = SimpleNamespace(user={"id": str(user_id), "is_active": True})

        response = dummy_handler(request=request)

        assert response == "OK"
