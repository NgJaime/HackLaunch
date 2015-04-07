from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage

def send_validation(strategy, backend, code):
    url = '{0}?verification_code={1}'.format(reverse('social:complete', args=(backend.name,)), code.code)
    absolute_url = strategy.request.build_absolute_uri(url)

    context = {
        'verification_url': absolute_url
    }

    html_message = get_template('verification_email.html').render(Context(context))
    email = EmailMessage('Validate your account', html_message, to=[code.email], from_email=settings.EMAIL_FROM)
    email.content_subtype = 'html'
    email.send()
