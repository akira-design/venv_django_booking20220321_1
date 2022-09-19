from datetime import datetime, date, timedelta, time
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localtime, make_aware
from django.views.generic import View, TemplateView, CreateView
from app.models import Store, Staff, Modality, Booking, Patient
from django.views.decorators.http import require_POST
from app.forms import BookingForm, PatientForm
from django.contrib.auth.mixins import LoginRequiredMixin
import calendar
# from collections import deque
# import itertools
from . import mixins
# from django.utils import timezone
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse_lazy


class TopView(TemplateView):
    template_name = 'app/top.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PatientInputView(View):
    def get(self, request, *args, **kwargs):
        form = PatientForm(request.POST or None)
        if request.user.is_authenticated:
            start_date = date.today()
            weekday = start_date.weekday()
            # カレンダー日曜日開始
            if weekday != 6:
                start_date = start_date - timedelta(days=weekday + 1)
            return redirect('mypage',  start_date.year, start_date.month, start_date.day)
        else:
            if request.GET:
                pt_id = request.GET['pt_id']
                pt_name = request.GET['pt_name']
                return render(request, 'app/patient_input.html', {
                    'form': form,
                    'pt_id': pt_id,
                    'pt_name': pt_name,
                })
            else:
                return render(request, 'app/patient_input.html', {
                    'form': form,
                })


    def post(self, request, *args, **kwargs):
        form = PatientForm(request.POST or None)
        pt_id = request.POST['pt_id']
        pt_name = request.POST['pt_name']
        if Patient.objects.filter(pt_id=pt_id).exists():
            messages.add_message(request, messages.ERROR, "すでに登録済みです。")
            return render(request, 'app/patient_input.html', {
                'form': form,
            })
        else:
            if form.is_valid():
                patient = Patient()
                patient.pt_id = form.cleaned_data['pt_id']
                patient.pt_name = form.cleaned_data['pt_name']
                patient.pt_gender = form.cleaned_data['pt_gender']
                patient.pt_birthday = form.cleaned_data['pt_birthday']
                patient.pt_remarks = form.cleaned_data['pt_remarks']
                patient.save()
                messages.add_message(request, messages.SUCCESS, "登録しました。")
                # store_data = Store.objects.all()
                redirect_url = reverse_lazy('store')
                parameters = urlencode(dict(
                    pt_id=pt_id,
                    pt_name=pt_name,
                ))
                url = f'{redirect_url}?{parameters}'
                return redirect(url)
                # return render(request, 'app/store.html', {
                #     'form': form,
                #     'store_data': store_data,
                    # 'pt_id': pt_id2,
                # })


class StoreView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            start_date = date.today()
            weekday = start_date.weekday()
            # カレンダー日曜日開始
            if weekday != 6:
                start_date = start_date - timedelta(days=weekday + 1)
            return redirect('mypage',  start_date.year, start_date.month, start_date.day)

        store_data = Store.objects.all()
        # form = PatientForm(request.POST or None)
        pt_id = request.GET['pt_id']
        pt_name = request.GET['pt_name']
        return render(request, 'app/store.html', {
            'store_data': store_data,
            # 'form': form,
            'pt_id': pt_id,
            'pt_name': pt_name,
        })


class StaffView(View):
    def get(self, request, *args, **kwargs):
        store_data = get_object_or_404(Store, id=self.kwargs['pk'])
        staff_data = Staff.objects.filter(store=store_data).select_related('user')
        pt_id = request.GET['pt_id']
        pt_name = request.GET['pt_name']

        return render(request, 'app/staff.html', {
            'store_data': store_data,
            'staff_data': staff_data,
            'pt_id': pt_id,
            'pt_name': pt_name,
        })


class ModalityView(View):
    def get(self, request, *args, **kwargs):
        store_data = get_object_or_404(Store, id=self.kwargs['pk'])
        staff_data = Staff.objects.filter(store=store_data).select_related('user')
        pt_id = request.GET['pt_id']
        pt_name = request.GET['pt_name']

        return render(request, 'app/staff.html', {
            'store_data': store_data,
            'staff_data': staff_data,
            'pt_id': pt_id,
            'pt_name': pt_name,
        })


class CalendarView(mixins.MonthWithScheduleMixin, mixins.WeekWithScheduleMixin, TemplateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'app/calendar.html'
    model = Booking, Staff
    date_field = 'date'
    time_field = 'start'
    staff_data = 'staff'
    opn = 8
    cls = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        staff_data = get_object_or_404(Staff, id=self.kwargs['pk'])
        pt_id = self.request.GET['pt_id']
        pt_name = self.request.GET['pt_name']
        # pt_name = Booking.objects.filter(staff=staff_data)
        context['staff_data'] = staff_data
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        return context


class BookingView(CalendarView):
    model = Booking, Patient
    form_class = PatientForm
    template_name = 'app/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        pt_id = self.request.GET['pt_id']
        pt_name = self.request.GET['pt_name']
        form = PatientForm()
        context['form'] = form
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        return context

    # def get(self, request, *args, **kwargs):
    #     staff_data = Staff.objects.filter(id=self.kwargs['pk']).select_related('user').select_related('store')[0]
    #     year = self.kwargs.get('year')
    #     month = self.kwargs.get('month')
    #     day = self.kwargs.get('day')
    #     hour = self.kwargs.get('hour')
    #     form = BookingForm(request.POST or None)
    #
    #     return render(request, 'app/booking.html', {
    #         'staff_data': staff_data,
    #         'year': year,
    #         'month': month,
    #         'day': day,
    #         'hour': hour,
    #         'form': form,
    #         # 'month_current': self.kwargs.get('current_month'),
    #         'week_previous': self.get_week_calendar(),
    #         'week_next': self.get_week_calendar(),
    #     })

    def post(self, request, *args, **kwargs):
        staff_data = get_object_or_404(Staff, id=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
        end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))
        date_field = date(year=year, month=month, day=day)
        booking_data = Booking.objects.filter(staff=staff_data, start=start_time)
        form = PatientForm(request.POST or None)
        pt_id = request.GET['pt_id']
        pt_name = request.GET['pt_name']
        pt_data = Patient.objects.get(pt_id=pt_id, pt_name=pt_name)
        if booking_data.exists():
            form.add_error(None, '既に予約があります。\n別の日時で予約をお願いします。')
        else:
            # if form.is_valid():
                booking = Booking()
                booking.staff = staff_data
                booking.start = start_time
                booking.end = end_time
                booking.date = date_field
                booking.pt_data = pt_data
                # booking.pt_id = pt_id
                # booking.pt_name = pt_name
                # booking.remarks = form.cleaned_data['remarks']
                booking.save()
                # return redirect('calendar', pk=staff_data.id)
                redirect_url = reverse_lazy('calendar', kwargs={'pk':staff_data.id})
                parameters = urlencode(dict(
                    pt_id=pt_id,
                    pt_name=pt_name,
                ))
                url = f'{redirect_url}?{parameters}'
                return redirect(url)

        return render(request, 'app/booking.html', {
            'staff_data': staff_data,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })

class ThanksView(TemplateView):
    template_name = 'app/thanks.html'


# class MyPageView(LoginRequiredMixin, CalendarView):
#     def get(self, request, *args, **kwargs):
#         # store_data = Store.objects.all()
#         staff_data = Staff.objects.filter(id=request.user.id).select_related('user').select_related('store')[0]
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')
#         day = self.kwargs.get('day')
#         start_date = date(year=year, month=month, day=day)
#         days = [start_date + timedelta(days=day) for day in range(7)]
#         start_day = days[0]
#         end_day = days[-1]
#
#         calendar = {}
#         # 10時～20時
#         for hour in range(self.opn, self.cls):
#             row = {}
#             for day_ in days:
#                 row[day_] = ""
#             calendar[hour] = row
#         start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))
#         end_time = make_aware(datetime.combine(end_day, time(hour=20, minute=0, second=0)))
#         booking_data = Booking.objects.filter(staff=staff_data).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
#         for booking in booking_data:
#             local_time = localtime(booking.start)
#             booking_date = local_time.date()
#             booking_hour = local_time.hour
#             if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
#                 calendar[booking_hour][booking_date] = booking.pt_data
#
#         # if request.user.groups.filter(name="放射線").exists():
#         #     modality_data = Modality.objects.filter(store=store_data)
#         return render(request, 'app/mypage.html', {
#             'staff_data': staff_data,
#             'booking_data': booking_data,
#             'calendar': calendar,
#             'days': days,
#             'start_day': start_day,
#             'end_day': end_day,
#             'before': days[0] - timedelta(days=7),
#             'next': days[-1] + timedelta(days=1),
#             'year': year,
#             'month': month,
#             'day': day,
#             'start_date': start_date,
#         })


# class MyPageView(LoginRequiredMixin, CalendarView):
#     template_name = 'app/mypage.html'
#     model = Booking, Staff
#     date_field = 'date'
#     time_field = 'start'
#     # staff_data = 'staff'
#     opn = 8
#     cls = 20
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         week_calendar_context = self.get_week_calendar()
#         # month_calendar_context = self.get_month_calendar()
#         # context.update(week_calendar_context)
#         # context.update(month_calendar_context)
#         staff_data = Staff.objects.filter(pk=self.request.user)
#         # pt_id = self.request.GET['pt_id']
#         # pt_name = self.request.GET['pt_name']
#         # # pt_name = Booking.objects.filter(staff=staff_data)
#         context['staff_data'] = staff_data
#         # context['pt_id'] = pt_id
#         # context['pt_name'] = pt_name
#         return context

@require_POST
def Holiday(request, year, month, day, hour):
    staff_data = Staff.objects.filter(id=request.user.id).select_related('user').select_related('store')[0]
    start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
    end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))
    date_field = date(year=year, month=month, day=day)

    # 予約追加
    Booking.objects.create(
        staff=staff_data,
        start=start_time,
        end=end_time,
        date=date_field,
    )

    start_date = date(year=year, month=month, day=day)
    weekday = start_date.weekday()
    # カレンダー日曜日開始
    if weekday != 6:
        start_date = start_date - timedelta(days=weekday + 1)
    return redirect('mypage', year=start_date.year, month=start_date.month, day=start_date.day)


@require_POST
def Delete(request, year, month, day, hour):
    start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
    booking_data = Booking.objects.filter(start=start_time)

    # 予約削除
    booking_data.delete()

    start_date = date(year=year, month=month, day=day)
    weekday = start_date.weekday()
    # カレンダー日曜日開始
    if weekday != 6:
        start_date = start_date - timedelta(days=weekday + 1)
    return redirect('mypage', year=start_date.year, month=start_date.month, day=start_date.day)
