# your_app/context_processors.py
from .models import Social

def social_links_processor(request):
    social = Social.objects.all()
    return dict(social=social)