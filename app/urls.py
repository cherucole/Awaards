from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^search/', views.search_results, name='search_results'),

    url(r'^$', views.homepage, name='homepage'),
    url(r'^upload$', views.add_post, name='add'),
    url(r'^accounts/profile/(?P<username>\w+)', views.profile, name='my_profile'),
    url(r'^post/(\d+)', views.get_individual_post, name='post'),

    # url(r'^search_results/', views.search_results, name='search'),
    # url(r'^like/(?P<operation>.+)/(?P<pk>\d+)', views.like, name='like'),
    url(r'^user/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^rate/(?P<pk>\d+)', views.rate_post, name='rate_post'),
    url(r'^new/profile$', views.add_profile, name='add_profile'),
    # url(r'^follow/(?P<operation>.+)/(?P<id>\d+)', views.follow, name='follow'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)