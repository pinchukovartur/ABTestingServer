from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from abtesting import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='abtesting/home.html'), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'abtesting/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'abtesting/logged_out.html'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test$', views.test, name='test'),
    url(r'^save/$', views.save_test, name='save_test')
]


"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    #url(r'', include('abtesting.urls')),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name='login')
    #url(r'^$', views.index, name='index'),
    #url(r'^save/$', views.save_test, name='save_test')

    #url(r'^auth/', include('loginsys.urls')),
]

"""