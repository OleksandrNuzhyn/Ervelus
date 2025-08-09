import threading


class ThreadIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print(f"SERVER STARTUP (Main Event Loop Thread ID): {threading.get_ident()}")

    def __call__(self, request):
        print(f"IN MIDDLEWARE (Worker Thread ID): {threading.get_ident()}")
        
        response = self.get_response(request)
        
        return response