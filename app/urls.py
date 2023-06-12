from django.urls import path
from app import views

urlpatterns = [
    path('', views.PatientInputView.as_view(), name='patient_input'),
    path('ct_order/', views.CtOrderView.as_view(), name='ct_order'),
    path('ct_order/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/', views.CtOrderView.as_view(), name='ct_order'),
    path('search/', views.PatientSearchView.as_view(), name='patient_search2'),
    path('store/', views.StoreView.as_view(), name='store'),
    path('store_list/', views.StoreListView.as_view(), name='store_list'),
    path('store/staff/<int:pk>/', views.StaffView.as_view(), name='staff'),
    path('store/modality/<int:pk>/', views.ModalityView.as_view(), name='modality'),
    path('mod_calendar/<int:pk>/', views.ModalityCalendarView.as_view(), name='mod_calendar'),
    path('mod_calendar/<int:pk>/<int:year>/<int:month>/<int:day>/', views.ModalityCalendarView.as_view(), name='mod_calendar'),
    path('mod_calendar/<int:pk>/<int:year>/<int:month>/', views.ModalityCalendarView.as_view(), name='mod_calendar'),
    path('mod_calendar/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/', views.ModalityCalendarView.as_view(), name='mod_calendar'),
    path('staff_calendar/<int:pk>/', views.StaffCalendarView.as_view(), name='staff_calendar'),
    path('staff_calendar/<int:pk>/<int:year>/<int:month>/<int:day>/', views.StaffCalendarView.as_view(), name='staff_calendar'),
    path('staff_calendar/<int:pk>/<int:year>/<int:month>/', views.StaffCalendarView.as_view(), name='staff_calendar'),
    # path('booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/', views.BookingView.as_view(), name='booking'),
    # path('booking/<int:pk>/<int:year>/<int:month>/<int:day>/', views.BookingView.as_view(), name='booking'),
    path('mod_booking/<int:pk>/<int:year>/<int:month>/<int:day>/', views.ModBookingView.as_view(), name='mod_booking'),
    path('mod_booking/', views.ModBookingView.as_view(), name='mod_booking'),
    path('mod_order/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/', views.ModBookingView.as_view(), name='mod_order'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),

    path('staff_booking/<int:pk>/<int:year>/<int:month>/<int:day>/', views.StaffBookingView.as_view(), name='staff_booking'),

    path('mod_booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/', views.ModBookingView.as_view(), name='mod_booking'),
    path('staff_booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/', views.StaffBookingView.as_view(), name='staff_booking'),
    path('thanks/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/', views.ThanksView.as_view(), name='thanks'),
    path('booking_list/', views.BookingListView.as_view(), name='booking_list'),
    path('mypage/<int:pk>/', views.MyPageView.as_view(), name='mypage'),
    path('mypage/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/', views.MyPageView.as_view(), name='mypage'),
    path('mypage/holiday/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Holiday, name='holiday'),
    path('mypage/delete/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Delete, name='delete'),
]
