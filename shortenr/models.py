from django.db import models
from django.urls import reverse

from settings import PRODUCTION_URL
from shortenr.fields.slug_field import AutoSlugField


class ShortenedUrl(models.Model):
    scheme = models.CharField(max_length=10, blank=True, null=True)
    path = models.TextField()
    query = models.TextField(null=True)
    url_slug = AutoSlugField(unique=True)

    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def original_url(self):
    	return "{0}://{1}{2}".format(
    		self.scheme, 
    		self.path, 
    		'?{0}'.format(self.query) if self.query else ''
    	)

    @property
    def rerouted_url(self):
    	# note that reverse returns the url with a forward slash at index 0
    	return PRODUCTION_URL + reverse('reroute', kwargs={'url_slug' : self.url_slug})

    @property
    def stat_url(self):
    	return reverse('home') + '?slug=' + self.url_slug


class ShortenedUrlStat(models.Model):
	url = models.ForeignKey(ShortenedUrl, on_delete=models.CASCADE)
	device = models.CharField(max_length=50, blank=True, null=True)
	browser = models.CharField(max_length=50, blank=True, null=True)
	ip_address = models.CharField(max_length=50, blank=True, null=True)

	viewed_on = models.DateTimeField(auto_now_add=True)