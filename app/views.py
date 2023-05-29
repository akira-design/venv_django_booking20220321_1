from datetime import datetime, date, timedelta, time
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localtime, make_aware
from django.views.generic import View, TemplateView, CreateView, ListView, UpdateView, DetailView
from app.models import Store, Staff, Modality, Booking, Patient, ParentCategory, Remark, Category
from django.views.decorators.http import require_POST
from app.forms import BookingForm, PatientForm, CtOrderCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
import calendar
# from collections import deque
# import itertools
from . import mixins
# from django.utils import timezone
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
import pytz


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
    fields = ('pt_id', 'pt_name', 'pt_gender', 'pt_birthday', 'pt_remarks')

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
        redirect_url = reverse_lazy('store_list')
        parameters = urlencode(dict(
            pt_id=patient.pt_id,
            pt_name=patient.pt_name,
        ))
        url = f'{redirect_url}?{parameters}'
        if Patient.objects.filter(pt_id=patient.pt_id):
            pt_data = Patient.objects.get(pt_id=patient.pt_id)
            if pt_data.pt_name == patient.pt_name:
                messages.add_message(self.request, messages.ERROR, "すでに登録済みです。")
                return redirect(url)
            else:
                messages.add_message(self.request, messages.ERROR, "IDが重複しています。氏名の確認お願いします。")
                return render(self.request, 'app/patient_input.html', {'form': form})
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


class StoreListView(StoreView):
    template_name = 'app/store_list.html'
    model = Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    template_name = 'app/modality.html'
    model = Modality

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_data = get_object_or_404(Store, id=self.kwargs['pk'])
        # staff_data = Staff.objects.filter(store=store_data).select_related('user')
        context.update({
            'modality_data': Modality.objects.filter(store=store_data),
        })
        pt_id = self.request.GET.get('pt_id')
        pt_name = self.request.GET.get('pt_name')
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        return context

    def get_queryset(self):
        return Store.objects.all()


class CalendarView(TemplateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    model = Booking
    date_field = 'date'
    # time_field = 'start'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pt_id = self.request.GET.get('pt_id')
        pt_name = self.request.GET.get('pt_name')
        # pt_name = Booking.objects.filter(staff=staff_data)
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        return context


class ModalityCalendarView(mixins.MonthWithModalityScheduleMixin, mixins.WeekWithModalityScheduleMixin, CalendarView):
    template_name = 'app/mod_calendar.html'
    opn = 10
    cls = 21
    interval = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        modality_data = get_object_or_404(Modality, pk=self.kwargs['pk'])

        if self.request.method == 'GET':
            category = self.request.GET.get('category')
            order_remarks = self.request.GET.get('order_remarks')
            parts = self.request.GET.get('parts')
            pt_id = self.request.GET.get('pt_id')
            pt_name = self.request.GET.get('pt_name')
            created_at = self.request.GET.get('created_at')
            # year = self.request.POST.get('year')
            # month = self.request.POST.get('month')
            # day = self.request.POST.get('day')
            # hour = self.request.POST.get('hour')
            # minute = self.request.POST.get('minute')
            # utc_time = datetime(year=year, month=month, day=day, hour=hour, minute=minute, tzinfo=pytz.UTC)
            # japan = pytz.timezone('Asia/Tokyo')
            # local_time = utc_time.astimezone(japan)

            # start_time = self.request.POST.get('start_time')

        else:
            category = None
            order_remarks = None
            parts = None
            pt_id = None
            pt_name = None
            created_at = None

        # context['start_time'] = start_time
        context['modality_data'] = modality_data
        context['category'] = category
        context['order_remarks'] = order_remarks
        context['parts'] = parts
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        context['created_at'] = created_at
        return context


class StaffCalendarView(mixins.MonthWithStaffScheduleMixin, mixins.WeekWithStaffScheduleMixin, CalendarView):
    template_name = 'app/staff_calendar.html'
    opn = 10
    cls = 16
    interval = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        staff_data = get_object_or_404(Staff, id=self.kwargs['pk'])
        context['staff_data'] = staff_data
        return context


class CtOrderView(CreateView):
    template_name = 'app/ct_order.html'

    model = Booking, Remark, Category
    form_class = CtOrderCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        minute = self.kwargs.get('minute')
        pt_id = self.request.GET.get('pt_id')
        pt_name = self.request.GET.get('pt_name')
        parts = self.request.GET.get('parts')
        category = self.request.GET.get('category')
        order_remarks = self.request.GET.get('order_remarks')
        context['year'] = year
        context['month'] = month
        context['day'] = day
        context['hour'] = hour
        context['minute'] = minute
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        context['category'] = category
        context['order_remarks'] = order_remarks
        context['parts'] = parts
        context['parentcategory_list'] = ParentCategory.objects.all()
        return context

    def form_valid(self, form):
        # modality_data = get_object_or_404(Modality, id=self.kwargs['pk'])
        modality_data = Modality.objects.get(name='CT')
        if self.kwargs.get('year'):
            year = self.kwargs.get('year')
            month = self.kwargs.get('month')
            day = self.kwargs.get('day')
            hour = self.kwargs.get('hour')
            minute = self.kwargs.get('minute')

            utc_time = datetime(year=year, month=month, day=day, hour=hour, minute=minute, tzinfo=pytz.UTC)
            japan = pytz.timezone('Asia/Tokyo')
            local_time = utc_time.astimezone(japan)

            start_time = local_time
            date_field = date(year=year, month=month, day=day)
        else:
            start_time = None

        pt_id = self.request.GET.get('pt_id')
        pt_data = Patient.objects.get(pt_id=pt_id)

        # order = form.save(commit=False)  # save form
        # order.order_remarks = form.cleaned_data['order_remarks']
        # order.category = form.cleaned_data['category']
        # order.parts = self.request.POST['parts']

        # parameters = urlencode(dict(
        #     category=form.cleaned_data['category'],
        #     order_remarks=form.cleaned_data['order_remarks'],
        #     parts=self.request.POST['parts'],
        # ))

        response = redirect('mod_calendar', pk=modality_data.pk)
        # get_params = self.request.GET.urlencode()
        # if self.request.GET.get('category') is None:
        #     response['location'] += '?' + get_params
        # else:
        # response['location']
        return response


class ModBookingView(CreateView):
    template_name = 'app/mod_booking.html'

    model = Booking, Remark, Category
    form_class = CtOrderCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modality = Modality.objects.get(pk=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        minute = self.kwargs.get('minute')
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour, minute=minute))

        if Booking.objects.filter(modality=modality, start=start_time):
            booking_data = Booking.objects.get(modality=modality, start=start_time)

            context['pt_id'] = booking_data.pt_data.pt_id
            context['pt_name'] = booking_data.pt_data.pt_name
            context['parts'] = booking_data.orders.parts
            context['category'] = booking_data.orders.category
            context['order_remarks'] = booking_data.orders.order_remarks
            context['created_at'] = booking_data.created_at
        else:
            category = self.request.GET.get('category')
            order_remarks = self.request.GET.get('order_remarks')
            parts = self.request.GET.get('parts')
            pt_id = self.request.GET.get('pt_id')
            pt_name = self.request.GET.get('pt_name')
            created_at = self.request.GET.get('created_at')
            context['pt_id'] = pt_id
            context['pt_name'] = pt_name
            context['parts'] = parts
            context['category'] = category
            context['order_remarks'] = order_remarks
            context['created_at'] = created_at

        context['modality_data'] = modality
        context['year'] = year
        context['month'] = month
        context['day'] = day
        context['hour'] = hour
        context['minute'] = minute
        context['parentcategory_list'] = ParentCategory.objects.all()
        return context

    def form_valid(self, form):
        modality_data = get_object_or_404(Modality, id=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        minute = self.kwargs.get('minute')
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour, minute=minute))
        date_field = date(year=year, month=month, day=day)
        created_at = self.request.GET.get('created_at')

        pt_id = self.request.GET.get('pt_id')
        pt_data = Patient.objects.get(pt_id=pt_id)

        # order = form.save(commit=False)  # save form

        if self.request.GET.get('category') is None:
            order_remarks = form.cleaned_data['order_remarks']
            category = form.cleaned_data['category']
            parts = self.request.POST['parts']
        else:
            cat = self.request.GET.get('category')
            category = Category.objects.get(name=cat)

            order_remarks = self.request.GET.get('order_remarks')

            parts = self.request.GET.get('parts')

        parameters = urlencode(dict(
            pt_id=pt_id,
            pt_name=pt_data.pt_name,
            category=category,
            parts=parts,
            order_remarks=order_remarks,
            # start=start_time.strftime('%Y年%m月%d日 %H時:%M分'),
            created_at=created_at
        ))

        booking_data = Booking.objects.filter(modality=modality_data, start=start_time)

        if booking_data.exists():
            messages.add_message(self.request, messages.ERROR, "すでに予約があります。")
            response = redirect('mod_calendar', pk=modality_data.pk)
            get_params = self.request.GET.urlencode()
            response['location'] += '?'+get_params + '&' + parameters
            return response
        else:
            if created_at == 'None':
                remarks = Remark()
                remarks.category = category
                remarks.order_remarks = order_remarks
                remarks.parts = parts
                remarks.save()

                orders = Remark.objects.get(pk=remarks.pk)
                booking_data = Booking()
                booking_data.modality = modality_data
                booking_data.start = start_time
                booking_data.date = date_field
                booking_data.pt_data = pt_data
                booking_data.orders_id = orders.pk
                booking_data.save()
                messages.add_message(self.request, messages.ERROR, "与薬完了")
            else:
                # created_date_string = self.object.created_at.strftime('%Y年%m月%d日%H:%M:%S')
                #
                # created_date_format = '%Y年%m月%d日%H:%M:%S'
                # created_date = datetime.strptime(created_date_string, created_date_format)
                created_date = created_at
                # created_at = Booking.objects.latest('created_at').created_at
                # created_at_date = datetime.strptime(created_at, '%Y年%m月%d日%H:%M')
                data = {
                    "start": start_time,
                    "date": date(
                        year=start_time.year,
                        month=start_time.month,
                        day=start_time.day
                    ),
                }
                if Booking.objects.filter(
                    created_at__year=created_date.year,
                    created_at__month=created_date.month,
                    created_at__day=created_date.day,
                    created_at__hour=created_date.hour,
                    created_at__minute=created_date.minute,
                    created_at__second=created_date.second
                ):
                    booking_data = Booking.objects.filter(
                        created_at__year=created_date.year,
                        created_at__month=created_date.month,
                        created_at__day=created_date.day,
                        created_at__hour=created_date.hour,
                        created_at__minute=created_date.minute,
                        created_at__second=created_date.second
                    )
                    booking_data.modality = modality_data
                    booking_data.update(**data)
                    messages.add_message(self.request, messages.ERROR, created_date)
                else:
                    messages.add_message(self.request, messages.ERROR, 'エラー')
                    booking_data.modality = modality_data

            # response = redirect('mod_calendar', pk=booking_data.modality.pk)
            # get_params = self.request.GET.urlencode()
            response = redirect('thanks')
            # get_params = self.request.GET.urlencode()
            # if self.request.GET.get('category') is None:
            response['location'] += '?' + parameters
            # elif self.request.POST.get('category'):
            #     response['location'] += '?' + get_params + '&' + parameters
            return response


class StaffBookingView(StaffCalendarView):
    model = Booking, Patient
    form_class = PatientForm
    template_name = 'app/staff_booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def post(self, request, *args, **kwargs):
        staff_data = get_object_or_404(Staff, id=self.kwargs['pk'])
        # modality_data = get_object_or_404(Modality, id=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        minute = self.kwargs.get('minute')

        utc_time = datetime(year=year, month=month, day=day, hour=hour, minute=minute, tzinfo=pytz.UTC)
        japan = pytz.timezone('Asia/Tokyo')
        local_time = utc_time.astimezone(japan)

        start_time = local_time

        if minute + self.interval < 60:
            minute = minute + self.interval
            end_time = local_time
        else:
            minute = minute + self.interval - 60
            end_time = local_time

        date_field = date(year=year, month=month, day=day)
        # booking_data = Booking.objects.filter(modality=modality_data, start=start_time)
        booking_data = Booking.objects.filter(staff=staff_data, start=start_time)
        form = BookingForm(request.POST or None)
        pt_id = request.GET['pt_id']
        pt_name = request.GET['pt_name']
        pt_data = Patient.objects.get(pt_id=pt_id)

        parameters = urlencode(dict(
            pt_id=pt_id,
            pt_name=pt_name,
            start=start_time,
        ))
        if booking_data.exists():
            messages.add_message(self.request, messages.ERROR, "すでに登録済みです。")
            redirect_url = reverse_lazy('store')
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
                url = f'{redirect_url}?{parameters}'
                return redirect(url)


class ThanksView(FormMixin, TemplateView):
    template_name = 'app/thanks.html'
    model = Booking

    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # POSTリクエストの処理
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pt_id = self.request.GET.get('pt_id') if self.request.method == 'GET' else self.request.POST.get('pt_id')
        pt_name = self.request.GET.get('pt_name') if self.request.method == 'GET' else self.request.POST.get('pt_name')
        start = self.request.GET.get('start') if self.request.method == 'GET' else self.request.POST.get('start')
        category = self.request.GET.get('category') if self.request.method == 'GET' else self.request.POST.get('category')
        parts = self.request.GET.get('parts') if self.request.method == 'GET' else self.request.POST.get('parts')
        order_remarks = self.request.GET.get('order_remarks') if self.request.method == 'GET' else self.request.POST.get('order_remarks')
        context['pt_id'] = pt_id
        context['pt_name'] = pt_name
        context['start'] = start
        context['category'] = category
        context['parts'] = parts
        context['order_remarks'] = order_remarks
        return context


class MyPageView(CalendarView):
    template_name = 'app/mypage.html'
    model = Booking, Staff
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookingListView(ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'
    ordering = ['date', 'start']


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
