from django.conf import settings

def static(request):
    return {
        'ex_static':settings.STATIC_URL,
    }