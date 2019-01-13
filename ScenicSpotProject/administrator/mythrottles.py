from rest_framework.throttling import SimpleRateThrottle


class MyThrottles(SimpleRateThrottle):
    scope = 'superadmin'
    THROTTLE_RATES = {
        'superadmin': '5/day'   # 5 次每天
    }

    def get_cache_key(self, request, view):
        user = request.user
        if user:
            ident = user
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }
