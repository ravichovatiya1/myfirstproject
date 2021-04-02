# https://github.com/shahraizali/awesome-django/blob/master/README.md#authentication
# https://godjango.com/

from django.urls import path,include
from blogs import views

app_name ='app'
urlpatterns = [
    path('', views.index_page,name = 'index'),

    path('register/', views.register, name='register'),
    path('otp_varify/', views.otp_varify, name='otp'),

    path('login/',views.user_login , name='login'),
    path('logout/',views.user_logout , name='logout'),

    path('profile/', views.user_profile, name= 'profile'),


    path('new_post/', views.PostCreateView.as_view(),name = 'post_create'),
    path('new_post/<int:pk>/', views.PostDetailView.as_view(),name = 'post_detail'),
    path('post/drafts/',views.DraftListView.as_view(),name = 'post_draft'),
    path('post/published/',views.PostListView.as_view(),name = 'post_list'),


    path('publish/<int:pk>/',views.post_publish,name = 'publish'),
    path('drafts/<int:pk>/',views.post_drafts, name = 'drafts'),

    path('postupdate/<int:pk>/', views.PostUpdateView.as_view(),name = 'post_update'),
    path('postdelete/<int:pk>/', views.PostDeleteView.as_view(),name = 'post_delete'),

    path('add_comment/<int:pk>/', views.add_comment,name = 'add_comment'),
]
