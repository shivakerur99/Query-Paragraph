from django.urls import path,include
from Codemonkuser.views import ParagraphListCreateAPIView, UserProfileView, UserRegistrationView,UserLoginView,ParagraphSearchAPIView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name="profile"),
    path('paragraphs/', ParagraphListCreateAPIView.as_view(), name='paragraph-list-create'),
    path('search/', ParagraphSearchAPIView.as_view(), name='paragraph-list-create'),
]