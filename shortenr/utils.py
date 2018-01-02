
import random
import re

def generate_slug(field):
    return slug_generator(field.max_length)


def generate_unique_slug(field, instance):
    # keep changing the slug until it is unique
    while True:
        # generate the slug
        slug = slug_generator(length=field.max_length)

        # find instances with same slug
        lookups = dict(**{field.name: slug})

        rivals = field.model._default_manager.filter(**lookups)

        if instance.pk:
            rivals = rivals.exclude(pk=instance.pk)

        if not rivals:
            # the slug is unique, no model uses it
            return slug

def slug_generator(length):
    return ''.join(random.choice('0123456789ABCDEF') for i in range(length))

def url_exists(url):
    ''' returns True if it does and False otherwise '''
    url_regex = re.compile("^(?:https?:\/\/)?(?:www\.)?[a-zA-Z0-9]+\..+$")
    return url_regex.match(url) != None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

