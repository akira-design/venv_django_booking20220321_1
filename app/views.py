from datetime import datetime, date, timedelta, time
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localtime, make_aware
from django.views.generic import View, TemplateView, CreateView, ListView
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


class PatientSearchView(ListView):
    template_name = 'app/patient_search2.html'
    # paginate_by = 5
    model = Booking, Patient

    # def post(self, request, *args, **kwargs):
    #     form_value = [
    #         self.request.POST.get('pt_id', None),
    #         # self.request.POST.get('text', None),
    #     ]
    #     request.session['form_value'] = form_value
    #     # 検索時にページネーションに関連したエラーを防ぐ
    #     self.request.GET = self.request.GET.copy()
    #     self.request.GET.clear()
    #     return self.get(request, *args, **kwargs)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
    #     pt_id = ''
    #     # pt_name = ''
    #     if 'form_value' in self.request.session:
    #         form_value = self.request.session['form_value']
    #         pt_id = form_value[0]
    #         # pt_name = form_value[1]
    #     default_data = {'pt_id': pt_id,  # タイトル
    #                     # 'pt_name': pt_name,  # 内容
    #                     }
    #     search_form = SearchForm(initial=default_data) # 検索フォーム
    #     context['search_form'] = search_form
    #     return context
    #
    # def get_queryset(self):
    #     # sessionに値がある場合、その値でクエリ発行する。
    #     if 'form_value' in self.request.session:
    #         form_value = self.request.session['form_value']
    #         pt_id = form_value[0]
    #         # pt_name = form_value[1]
    #         # 検索条件
    #         condition_pt_id = Q()
    #         # condition_text = Q()
    #         if len(pt_id) != 0 and pt_id[0]:
    #             condition_pt_id = Q(pt_id__icontains=pt_id)
    #         # if len(text) != 0 and text[0]:
    #         #     condition_text = Q(text__contains=text)
    #         pt_data = Patient.objects.get(pt_id=condition_pt_id)
    #         return Booking.objects.filter(pt_data = pt_data)
    #     else:
    #         # 何も返さない
    #         return Booking.objects.none()


    def get_queryset(self):
        queryset = Booking.objects.order_by('-id')
        keyword = self.request.GET.get('keyword')

        if keyword:
            if Patient.objects.filter(pt_id=keyword):
                pt_data = Patient.objects.get(pt_id=keyword)
            # if pt_data:
                queryset = queryset.filter(Q(pt_data_id=pt_data))
                if queryset:
                    messages.success(self.request, '検索結果')
                else:
                    messages.error(self.request, '登録情報なし')
                return queryset
            else:
                # raise Http404("No User matches the given query.")
                messages.error(self.request, '登録情報なし')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        if keyword:
            if Patient.objects.filter(pt_id=keyword):
                pt_data = Patient.objects.get(pt_id=keyword)
                context['pt_data'] = pt_data
        return context


class PatientInputView(CreateView):
    template_name = 'app/patient_input.html'
    model = Patient
    fields = ('pt_id','pt_name','pt_gender','pt_birthday','pt_remarks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PatientForm()
        # if self.request.GET:
        #     pt_id = self.request.GET['pt_id']
        #     pt_name = self.request.GET['pt_name']
        #     context['pt_id'] = pt_id
        #     context['pt_name'] = pt_name
        # else:
        context['form'] = form
        return context

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.pt_id = form.cleaned_data['pt_id']
        patient.pt_name = form.cleaned_data['pt_name']
        patient.pt_gender = form.cleaned_data['pt_gender']
        patient.pt_birthday = form.cleaned_data['pt_birthday']
        patient.pt_remarks = form.cleaned_data['pt_remarks']
        redirect_url = reverse_lazy('store')
        parameters = urlencode(dict(
            pt_id=patient.pt_id,
            pt_name=patient.pt_name,
        ))
        url = f'{redirect_url}?{parameters}'
        if Patient.objects.filter(pt_id=patient.pt_id):
            if Patient.objects.filter(pt_name=patient.pt_name):
                messages.add_message(self.request, messages.ERROR, "すでに登録済みです。")
                return redirect(url)
            else:
                messages.add_message(self.request, messages.ERROR, "IDが重複しています。氏名の確認お願いします。")
                return redirect('/')
        else:
            patient.save()
            messages.add_message(self.request, messages.SUCCESS, "登録しました。")
            return redirect(url)


# class StoreView(View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             start_date = date.today()
#             weekday = start_date.weekday()
#             # カレンダー日曜日開始
#             if weekday != 6:
#                 start_date = start_date - timedelta(days=weekday + 1)
#             return redirect('mypage',  start_date.year, start_date.month, start_date.day)
#
#         store_data = Store.objects.all()
#         # form = PatientForm(request.POST or None)
#         pt_id = request.GET['pt_id']
#         pt_name = request.GET['pt_name']
#         return render(request, 'app/store.html', {
#             'store_data': store_data,
#             # 'form': form,
#             'pt_id': pt_id,
#             'pt_name': pt_name,
#         })


class StoreView(ListView):
    template_name = 'app/store.html'
    model = Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pt_id = self.request.GET.get('pt_id')
        pt_name = self.request.GET.get('pt_name')
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        return context


# class StaffView(View):
#     def get(self, request, *args, **kwargs):
#         store_data = get_object_or_404(Store, id=self.kwargs['pk'])
#         staff_data = Staff.objects.filter(store=store_data).select_related('user')
#         pt_id = request.GET['pt_id']
#         pt_name = request.GET['pt_name']
#
#         return render(request, 'app/staff.html', {
#             'store_data': store_data,
#             'staff_data': staff_data,
#             'pt_id': pt_id,
#             'pt_name': pt_name,
#         })

class StaffView(ListView):
    template_name = 'app/staff.html'
    model = Staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_data = get_object_or_404(Store, id=self.kwargs['pk'])
        staff_data = Staff.objects.filter(store=store_data).select_related('user')
        context.update({
            'staff_data': staff_data,
        })
        pt_id = self.request.GET.get('pt_id')
        pt_name = self.request.GET.get('pt_name')
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        return context

    def get_queryset(self):
        return Store.objects.all()


# class ModalityView(View):
#     def get(self, request, *args, **kwargs):
#         store_data = get_object_or_404(Store, id=self.kwargs['pk'])
#         staff_data = Staff.objects.filter(store=store_data).select_related('user')
#         pt_id = request.GET['pt_id']
#         pt_name = request.GET['pt_name']
#
#         return render(request, 'app/staff.html', {
#             'store_data': store_data,
#             'staff_data': staff_data,
#             'pt_id': pt_id,
#             'pt_name': pt_name,
#         })

class ModalityView(ListView):
    template_name = 'app/staff.html'
    model = Modality

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_data = get_object_or_404(Store, id=self.kwargs['pk'])
        # staff_data = Staff.objects.filter(store=store_data).select_related('user')
        context.update({
            'staff_data': Staff.objects.filter(store=store_data).select_related('user'),
        })
        pt_id = self.request.GET.get('pt_id')
        pt_name = self.request.GET.get('pt_name')
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        return context

    def get_queryset(self):
        return Store.objects.all()


class CalendarView(mixins.MonthWithScheduleMixin, mixins.WeekWithScheduleMixin, TemplateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'app/calendar.html'
    model = Booking
    date_field = 'date'
    # time_field = 'start'
    opn = 8
    cls = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        staff_data = get_object_or_404(Staff, id=self.kwargs['pk'])
        pt_id = self.request.GET.get('pt_id')
        pt_name = self.request.GET.get('pt_name')
        # pt_name = Booking.objects.filter(staff=staff_data)
        context['staff_data'] = staff_data
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        return context


class RihabiriCalendarView(CalendarView):
    opn = 10
    cls = 23

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_data = get_object_or_404(Staff, id=self.kwargs['pk'])
        context['staff_data'] = staff_data
        return context

class BookingView(CalendarView):
    model = Booking, Patient
    form_class = PatientForm
    template_name = 'app/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PatientForm()
        context['form'] = form
        return context

    # def post(self, request, *args, **kwargs):
    #     return redirect(url)
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
        form = BookingForm(request.POST or None)
        pt_id = request.GET['pt_id']
        pt_name = request.GET['pt_name']
        pt_data = Patient.objects.get(pt_id=pt_id)
        if booking_data.exists():
            messages.add_message(self.request, messages.ERROR, "すでに登録済みです。")
            redirect_url = reverse_lazy('store')
            parameters = urlencode(dict(
                pt_id=pt_id,
                pt_name=pt_name,
                start=start_time,
            ))
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
        else:
            if form.is_valid():
                booking = Booking()
                booking.staff = staff_data
                booking.start = start_time
                booking.end = end_time
                booking.date = date_field
                booking.pt_data = pt_data
                booking.save()
                redirect_url = reverse_lazy('thanks')
                parameters = urlencode(dict(
                    pt_id=pt_id,
                    pt_name=pt_name,
                    start=start_time,
                ))
                url = f'{redirect_url}?{parameters}'
                return redirect(url)


    # def form_valid(self, form):
    #     patient = form.save(commit=False)
    #     patient.pt_id = form.cleaned_data['pt_id']
    #     patient.pt_name = form.cleaned_data['pt_name']
    #     patient.pt_gender = form.cleaned_data['pt_gender']
    #     patient.pt_birthday = form.cleaned_data['pt_birthday']
    #     patient.pt_remarks = form.cleaned_data['pt_remarks']
    #     if Patient.objects.filter(pt_id=patient.pt_id):
    #         messages.add_message(self.request, messages.ERROR, "すでに登録済みです。")
    #         return redirect('/')
    #     else:
    #         patient.save()
    #         messages.add_message(self.request, messages.SUCCESS, "登録しました。")
    #         redirect_url = reverse_lazy('store')
    #         parameters = urlencode(dict(
    #             pt_id=patient.pt_id,
    #             pt_name=patient.pt_name,
    #         ))
    #         url = f'{redirect_url}?{parameters}'
    #         return redirect(url)


class ThanksView(TemplateView):
    template_name = 'app/thanks.html'
    model = Booking

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pt_id = self.request.GET.get('pt_id')
        pt_name = self.request.GET.get('pt_name')
        start = self.request.GET.get('start')
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        context['start'] = start
        return context


class MyPageView(CalendarView):
    template_name = 'app/mypage.html'
    model = Booking, Staff
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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

    # start_date = datetime(year=year, month=month, day=day, hour=hour)
    # weekday = start_date.weekday()
    # # カレンダー日曜日開始
    # if weekday != 6:
    #     start_date = start_date - timedelta(days=weekday + 1)
    # pt_id = request.GET.get('pt_id')
    return redirect('mypage', pk=staff_data.pk, year=start_time.year, month=start_time.month, day=start_time.day, hour=start_time.hour)


@require_POST
def Delete(request, year, month, day, hour):
    staff_data = Staff.objects.filter(id=request.user.id).select_related('user').select_related('store')[0]
    start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
    booking_data = Booking.objects.filter(start=start_time)

    # 予約削除
    booking_data.delete()

    # start_date = date(year=year, month=month, day=day)
    # weekday = start_date.weekday()
    # # カレンダー日曜日開始
    # if weekday != 6:
    #     start_date = start_date - timedelta(days=weekday + 1)
    return redirect('mypage', pk=staff_data.pk, year=start_time.year, month=start_time.month, day=start_time.day, hour=start_time.hour)
