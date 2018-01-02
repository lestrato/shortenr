
from django.db.models.fields import CharField
from shortenr.utils import generate_slug, generate_unique_slug

DEFAULT_MAX_LENGTH = 7

class AutoSlugField(CharField):
    """
    AutoSlugField is an extended CharField able to automatically resolve name
    clashes.

    AutoSlugField can also perform the following tasks on save:

    - preserve uniqueness of the value (using `unique`).

    None of the tasks is mandatory, i.e. you can have auto-populated non-unique
    fields, manually entered unique ones (absolutely unique or within a given
    date) or both.

    Uniqueness is preserved by check if the the slug is used in the same field in the same
    model

    :param unique: boolean: ensure total slug uniqueness (unless more precise
        `unique_with` is defined).

    .. note:: always place any slug attribute *after* attributes referenced
        by it (i.e. those from which you wish to `populate_from` or check
        `unique_with`). The reasoning is that autosaved dates and other such
        fields must be already processed before using them in the AutoSlugField.

    Example usage:

    .. code-block:: python

        from django.db import models
        from fields import AutoSlugField

        class Article(models.Model):
            '''An article with title, date and slug. The slug is not totally
            unique but there will be no two articles with the same slug within
            any month.
            '''
            title = models.CharField(max_length=200)
            pub_date = models.DateField(auto_now_add=True)
            slug = AutoSlugField(unique=True)


    More options:

    .. code-block:: python

        # slugify but allow non-unique slugs
        slug = AutoSlugField()

        # globally unique, silently fix on conflict ("foo" --> "foo-1".."foo-n")
        slug = AutoSlugField(unique=True)

        # globally unique, silently fix on conflict ("foo" --> "foo-1".."foo-n")
        slug = AutoSlugField(unique=True)
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', DEFAULT_MAX_LENGTH)
        kwargs['unique'] = kwargs.get('unique', False)

        super(AutoSlugField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(AutoSlugField, self).deconstruct()

        if self.max_length == DEFAULT_MAX_LENGTH:
            kwargs.pop('max_length', None)

        if self.unique == False:
            kwargs.pop('unique', None)

        return name, path, args, kwargs

    def pre_save(self, instance, add):
        # ensure the slug is unique (if required)
        if self.unique:
            slug = generate_unique_slug(field=self, instance=instance)
        else:
            slug = generate_slug(field=self)

        # make the updated slug available as instance attribute
        setattr(instance, self.name, slug)

        return slug
