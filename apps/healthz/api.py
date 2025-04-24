from ninja import Router

healthz_router = Router()

@healthz_router.get("")
def check_sys_health(request):
    return "System is up and running..."