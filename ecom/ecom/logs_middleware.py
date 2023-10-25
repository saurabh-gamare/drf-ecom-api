import json
from accounts.models import Log


class LogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log_id = self.log_request(request)

        response = self.get_response(request)

        self.log_response(response, log_id)
        return response

    def log_request(self, request):
        try:
            endpoint = request.path
        except:
            endpoint = ''
        if not endpoint.startswith('/api/v1/'):
            return ''
        try:
            headers = dict(request.headers)
        except:
            headers = {}
        try:
            if request.method == 'GET':
                payload = dict(request.GET)
            else:
                payload = json.loads(request.body.decode('utf-8'))
        except:
            payload = {}
        try:
            instance = Log(endpoint=endpoint, request=payload, headers=headers)
            instance.save()
            return instance.id
        except:
            return ''

    def log_response(self, response, log_id):
        if not log_id:
            return
        try:
            res = dict(response.data)
        except:
            res = {}
        Log.objects.filter(id=log_id).update(response=res)
        return ''
