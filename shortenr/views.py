
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView, View
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import redirect, get_object_or_404

import json
import settings
import os
from urlparse import urlparse
from collections import OrderedDict
from datetime import datetime, timedelta

from shortenr.models import ShortenedUrl, ShortenedUrlStat
from shortenr.utils import url_exists, get_client_ip

class LandingPageView(TemplateView):
    '''
    This view handles all invoice transactions except purchasing new seats onto an existing subscription.
    '''
    template_name = 'shortenr/index.html'

    def get(self, *args, **kwargs):

        return super(LandingPageView, self).get(*args, **kwargs)

    def get_stat_data(self, *args, **kwargs):
        context = super(
            LandingPageView, self).get_context_data(*args, **kwargs)

        # get stat
        slug = self.request.GET.get('slug', None)
        if not slug: return context

        try:
            url = ShortenedUrl.objects.get(url_slug=slug)
        except ShortenedUrl.DoesNotExist:
            context['slug_found'] = False
            return context

        context['url_object'] = url

        stat_set = url.shortenedurlstat_set.all().order_by('viewed_on')

        browser_families = []
        browser_family_counts = []
        for browser in set(stat_set.values_list('browser', flat=True)):
            browser_families.append(browser)
            browser_family_counts.append(stat_set.filter(browser=browser).count())
        context['total_browser_count'] = browser_families
        context['browser_families'] = json.dumps(browser_families)
        context['browser_family_counts'] = json.dumps(browser_family_counts)

        device_families = []
        device_family_counts = []
        for device in set(stat_set.values_list('device', flat=True)):
            device_families.append(device)
            device_family_counts.append(stat_set.filter(device=device).count())
        context['total_device_count'] = device_families
        context['device_families'] = json.dumps(device_families)
        context['device_family_counts'] = json.dumps(device_family_counts)

        context['all_stats'] = stat_set
        return context

    def get_context_data(self, *args, **kwargs):
        context = super(
            LandingPageView, self).get_context_data(*args, **kwargs)

        context = self.get_stat_data(*args, **kwargs)

        url = os.path.join(settings.BASE_DIR, 'static', 'vendor/particles/particles-config.json')
        json_data = open(url)   
        particle_config = json.load(json_data) # deserialises it
        json_data.close()

        context['particle_config'] = json.dumps(particle_config)

        print context
        return context

    def post(self, *args, **kwargs):
        
        if self.request.is_ajax():
            url = self.request.POST.get('url').strip()

            url_parse = urlparse(url)
            # >>> url
            # ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
            #             params='', query='', fragment='')

            path = ''
            if url_parse.netloc: path += url_parse.netloc
            if url_parse.path: path += url_parse.path

            scheme = 'http' # default it to http
            if url_parse.scheme: scheme = url_parse.scheme

            query = None
            if url_parse.query: query = url_parse.query

            if settings.PRODUCTION_URL in path:
                return JsonResponse({
                    'message': "You can't shorten a Shortenr link."
                })

            if not path or not url_exists(url):
                return JsonResponse({
                    'message': 'You must provide a valid URL for us to shorten.'
                })

            new_url = ShortenedUrl(
                scheme=scheme,
                path=path,
                query=query,
            )
            new_url.save()
            return JsonResponse({ 'reroute_url': new_url.rerouted_url, 'stat_url': new_url.stat_url})
        return super(LandingPageView, self).get(*args, **kwargs)

class UrlReroutePageView(View):

    def dispatch(self, *args, **kwargs):
        url = get_object_or_404(ShortenedUrl, url_slug=kwargs.get('url_slug'))
        
        browser_family = self.request.user_agent.browser.family  # returns 'Mobile Safari'
        device_family = self.request.user_agent.device.family # returns 'iPhone'
        ip_address = get_client_ip(self.request)

        # save the stat
        new_url_stat = ShortenedUrlStat(
            url=url,
            device=device_family,
            browser=browser_family,
            ip_address=ip_address,
        )

        new_url_stat.save()

        return redirect(url.original_url)

def api_get_url(request):
    slug = request.GET.get('slug', None)
    print slug
    try:
        if not slug: raise ShortenedUrl.DoesNotExist
        url = ShortenedUrl.objects.get(url_slug=slug)
    except ShortenedUrl.DoesNotExist:
        return JsonResponse({'found':'false'}, status=404)

    return JsonResponse({'found':'true'}, status=200)
