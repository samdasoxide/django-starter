"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import, unicode_literals

from django.conf import settings
{% if cookiecutter.wagtail == "y" -%}
from django.conf.urls import include, url
{% else -%}
from django.conf.urls import url
{% endif -%}
from django.contrib import admin
{%- if cookiecutter.wagtail == "n" %}
from django.views.generic import TemplateView
{%- endif %}
{% if cookiecutter.wagtail == "y" -%}

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
{%- endif %}

{% if cookiecutter.wagtail == "y" -%}
urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'', include(wagtail_urls)),
]
{% else -%}
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="base.html")),
    url(r'^admin/', admin.site.urls),
]
{%- endif %}

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
