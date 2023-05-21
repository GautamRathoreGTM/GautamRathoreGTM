

from django.urls import path
from .views import *
from .API import *

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('get-users', UsersView.as_view(), name="get_user" ),
    path('create-users', CeateUserView.as_view(), name="create_user" ),
    path('delete-users', DeleteUserView.as_view(), name="create_user" ),



# use bearer token for them : mf8nrqICaHYD1y8wRMBksWm7U7gLgXy1mSWjhI0q
    # ddos
    path('validate/', DDOSValidatorView.as_view(), name='validate'),
    # bearer
    path('authenticate/', BearerAuthView.as_view(), name='authenticate'),

]
