from django.urls import path
from app import views

urlpatterns = [
    path('', views.PatientInputView.as_view(), name='patient_input'),
    path('search/', views.PatientSearchView.as_view(), name='patient_search2'),
    path('store/', views.StoreView.as_view(), name='store'),
    path('store/staff/<int:pk>/', views.StaffView.as_view(), name='staff'),
    path('store/modality/<int:pk>/', views.ModalityView.as_view(), name='modality'),
    path('calendar/<int:pk>/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/<int:pk>/<int:year>/<int:month>/<int:day>/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/<int:pk>/<int:year>/<int:month>/', views.CalendarView.as_view(), name='calendar'),
    path('booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/', views.BookingView.as_view(), name='booking'),
    path('booking/<int:pk>/<int:year>/<int:month>/<int:day>/', views.BookingView.as_view(), name='booking'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('mypage/<int:pk>/<int:year>/<int:month>/<int:day>/', views.MyPageView.as_view(), name='mypage'),
    path('mypage/<int:pk>/', views.MyPageView.as_view(), name='mypage'),
    path('mypage/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/', views.MyPageView.as_view(), name='mypage'),
    path('mypage/holiday/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Holiday, name='holiday'),
    path('mypage/delete/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Delete, name='delete'),
]
