from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.generic import TemplateView


from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^loginuser/', views.loginuser, name='loginuser'),
    url(r'^logoutuser/',auth_views.LogoutView.as_view(template_name='reload/logged_out.html'),name='logoutuser'),

    url(r'^contact/',views.ContactFormView.as_view(),name='contact'),
    url(r'^contact_send/',TemplateView.as_view(template_name='reload/contact_sent.html'),name='contact_sent'),

    url(r'^password_change/', views.password_change, name='password_change'),
    url(r'^password_reset/', auth_views.PasswordResetView.as_view(template_name='reload/password_reset.html', from_email=settings.DEFAULT_FROM_EMAIL),name='password_reset'),
    url(r'^password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='reload/password_reset_done.html'),name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reload/password_reset_complete.html'),name='password_reset_complete'),


    url(r'^bede_wpisywal_dane/',views.create_user, name='create_user'),
    url(r'^registeruser/', views.create_user, name='registeruser'),

    url(r'^whats_new/', views.whats_new, name='whats_new'),

    # url(r'^loads/', views.loaddata, name='loads'),
    url(r'^loads/', views.LoadFilteredTable.as_view(), name='loads'),
    url(r'^load_new/', views.load_new, name='load_new'),
    url(r'^load_edit/(?P<key>\d+)/', views.load_edit, name='load_edit'),

    url(r'^load_comment_test/(?P<key>\d+)/', views.load_comment_test, name='load_comment_test'),
    url(r'^comment_edit/(?P<key>\d+)/(?P<id_load>\d+)/', views.comment_edit, name='comment_edit'),
    url(r'^test_new/(?P<key>\d+)/', views.test_new, name='test_new'),
    url(r'^test_edit/(?P<key>\d+)/(?P<id_load>\d+)/', views.test_edit, name='test_edit'),

    url(r'^load_by_powder/(?P<key>\d+)/', views.load_by_powder, name='load_by_powder'),
    url(r'^load_by_caliber/(?P<key>\d+)/', views.load_by_caliber, name='load_by_caliber'),
    url(r'^load_by_bullet/(?P<key>\d+)/', views.load_by_bullet, name='load_by_bullet'),

    url(r'^calibers/', views.calibers, name='calibers'),
    url(r'^caliber_new/', views.caliber_new, name='caliber_new'),
    url(r'^caliber_edit/(?P<key>\d+)/', views.caliber_edit, name='caliber_edit'),

    url(r'^bullets/', views.BulletFilteredTable.as_view(), name='bullets'),
    url(r'^bullet_new/', views.bullet_new, name='bullet_new'),
    url(r'^bullet_edit/(?P<key>\d+)/', views.bullet_edit, name='bullet_edit'),

    url(r'^powders/', views.PowderFilteredTable.as_view(), name='powders'),
    url(r'^powder_new/', views.powder_new, name='powder_new'),
    url(r'^powder_edit/(?P<key>\d+)/', views.powder_edit, name='powder_edit'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
