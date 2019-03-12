from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from API.views import UserViewSet, PostViewSet, LikeViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

users_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
users_router.register(r'posts', PostViewSet, basename='user-posts')

posts_router = routers.NestedDefaultRouter(users_router, r'posts', lookup='post')
posts_router.register(r'likes', LikeViewSet, basename='post-likes')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(users_router.urls)),
    path('api/', include(posts_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
