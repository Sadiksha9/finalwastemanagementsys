from django.urls import path
from core.views import home, scan, contact, complain
from core.views import WasteImageListView, WasteImageDetailView, WasteImageUploadView
from core.auth import signup, login_view, logout_view
from core.email import report_waste  # Ensure this import is correct

urlpatterns = [
    path('', home, name='home'),
    path('scan/', scan, name='scan'),
    path('contact/', contact, name='contact'),
    path('complain/', complain, name='complain'),
    path('waste', WasteImageListView.as_view(), name='waste-list'),
    path('waste/upload/', WasteImageUploadView.as_view(), name='waste-upload'),
    path('detail/<int:pk>/', WasteImageDetailView.as_view(), name='waste-detail'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('report-waste/', report_waste, name='report-waste'),  # Uncommented this line
]