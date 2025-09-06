from django.utils import translation
from django.conf import settings

def language_processor(request):
    """Context processor to ensure language is properly set"""
    language = request.session.get('django_language', settings.LANGUAGE_CODE)
    if language in [lang[0] for lang in settings.LANGUAGES]:
        translation.activate(language)
    return {
        'LANGUAGE_CODE': language,
        'LANGUAGES': settings.LANGUAGES,
    }
