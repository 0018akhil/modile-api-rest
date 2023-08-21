from django.urls import path
from .views import UserSignUp, UserSignIn, userSearch, spam, NotFoundView, addEmail

urlpatterns = [
    path('signup', UserSignUp.as_view(), name='signup'),
    path('signin', UserSignIn.as_view(), name='signin'),
    path('search', userSearch.as_view(), name='search'),
    path('spam', spam.as_view(), name='spam'),
    path('addemail', addEmail.as_view(), name='addemail'),
    path('', NotFoundView.as_view(), name='not_found'),
]