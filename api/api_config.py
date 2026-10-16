class APIConfig:
    ENDPOINTS = {
        'login': '/api/auth/login',
        'register': '/api/auth/register',
        'send_code': '/api/auth/send-code',
        'verify_email': '/api/auth/verify-email',
        'users': '/api/users'
    }
    
    def get_endpoint_url(self, endpoint_name):
        return self.ENDPOINTS.get(endpoint_name, '')
