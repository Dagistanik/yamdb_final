from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'users', views.UsersViewSet)

router.register(r'genres', views.GenreViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'titles', views.TitleViewSet, basename='titles')

router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = (
    path('v1/users/me/', views.MeViewSet.as_view()),
    path('v1/auth/signup/', views.send_confirmation_code, name='signup'),
    path('v1/auth/token/', views.get_token, name='token'),
    path('v1/', include(router.urls)),

)
