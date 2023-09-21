from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import (CompanyListCreateView, CompanyRetrieveUpdateDestroyView,
                    DepartmentListCreateView,
                    DepartmentRetrieveUpdateDestroyView,
                    EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView,
                    RoleListCreateView, RoleRetrieveUpdateDestroyView)

app_name = 'api'

urlpatterns = [
    path('user-profile/<str:username>/', views.user_profile, name='user_profile'),
    path('company-details/<int:company_id>/', views.company_details, name='company_details'),
    path('department-details/<int:department_id>/', views.department_details, name='department_details'),
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyView.as_view(), name='role-retrieve-update-destroy'),
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyRetrieveUpdateDestroyView.as_view(), name='company-retrieve-update-destroy'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyView.as_view(), name='department-retrieve-update-destroy'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-retrieve-update-destroy'),
    path('single_entry_update/', views.single_entry_update, name='single_entry_update'),
    path('bulk_upload/', views.BulkUploadView.as_view(), name='bulk_upload'),
    path('bulk_upload/success/', views.bulk_upload_success, name='bulk_upload_success'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)