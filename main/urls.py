from django.conf.urls import url
from main import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^requests/$', views.requests, name='requests'),
    url(r'^ajax/getRequests/$', views.ajaxGetRequests, name='get_requests'),
    url(r'^downloadResults/$', views.download_results, name='download_results'),
    url(r'^downloadLogs/$', views.download_logs, name='download_logs'),
]