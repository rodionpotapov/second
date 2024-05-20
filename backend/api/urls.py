from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from . import views


app_name = 'api'

get_schema_view = get_schema_view(
    openapi.Info(
        title="Big Corp API",
        default_version='v1',
        description="Big Corp API description",
        terms_of_service= "https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rodionpotapov@icloud.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)




urlpatterns = [
    #products
    path('products/',views.ProductListApiView.as_view() , name = 'product-list'),
    path('products/<int:pk>/',views.ProductDetailAPIView.as_view() , name = 'product-detail'),

    path('reviews/create/', views.ReviewCreateView.as_view()),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('swagger/', get_schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', get_schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
