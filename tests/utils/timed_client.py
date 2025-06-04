import time
from rich import print


class TimedClient:
    def __init__(self, client):
        self.client = client
    def _log_timing(self, method_name, url, start):
        duration = time.perf_counter() - start
        print(f"\n[{method_name.upper()}] {url} - {duration:.4f}s")

    def get(self, *args, **kwargs):
        start = time.perf_counter()
        response = self.client.get(*args, **kwargs)
        self._log_timing("get", args[0], start)
        return response

    def post(self, *args, **kwargs):
        start = time.perf_counter()
        response = self.client.post(*args, **kwargs)
        self._log_timing("post", args[0], start)
        return response

    def patch(self, *args, **kwargs):
        start = time.perf_counter()
        response = self.client.patch(*args, **kwargs)
        self._log_timing("patch", args[0], start)
        return response

    def put(self, *args, **kwargs):
        start = time.perf_counter()
        response = self.client.put(*args, **kwargs)
        self._log_timing("put", args[0], start)
        return response

    def delete(self, *args, **kwargs):
        start = time.perf_counter()
        response = self.client.delete(*args, **kwargs)
        self._log_timing("delete", args[0], start)
        return response