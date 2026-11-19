from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


def api_index(request):
    return JsonResponse({
        'message': 'Threadline API is running.',
        'endpoints': {
            'products': '/api/products/',
            'register': '/api/auth/register/',
            'login': '/api/auth/login/',
            'cart': '/api/cart/',
            'checkout': '/api/checkout/',
            'transactions': '/api/transactions/',
            'admin': '/admin/',
        },
    })


urlpatterns = [
    path('', api_index, name='api-index'),
    path('api/', api_index, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
