from apps.users.models import UserModel
from http import HTTPStatus
from ninja.errors import HttpError

def require_active_user(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.user["id"]
            user = UserModel.objects.get(id=user_id)
        except Exception:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "User does not exist")
        
        if not user.is_active:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "User is inactive")
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
        
