from django import forms
from .models import Booking, Patient, ParentCategory, Remark


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('pt_data',)
        # first_name = forms.CharField(max_length=30, label='姓')
        # last_name = forms.CharField(max_length=30, label='名')
        # tel = forms.CharField(max_length=30, label='電話番号')
        # remarks = forms.CharField(label='備考', widget=forms.Textarea())


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('pt_id', 'pt_name', 'pt_gender', 'pt_birthday', 'pt_remarks')
        widgets = {
            'pt_remarks': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class SearchForm(forms.Form):
    pt_id = forms.IntegerField(
        initial='',
        label='ID',
        required=False, # 必須ではない
        widget=forms.TextInput(attrs={'placeholder': '検索ID'})
    )
    # text = forms.CharField(
    #     initial='',
    #     label='内容',
    #     required=False,  # 必須ではない
    # )


class CtOrderCreateForm(forms.ModelForm):
    # 親カテゴリの選択欄がないと絞り込めないので、定義する。
    parent_category = forms.ModelChoiceField(
        label='親カテゴリ',
        queryset=ParentCategory.objects,
        required=False
    )

    class Meta:
        model = Remark
        fields = ('parent_category', 'category', 'order_remarks')
        widgets = {
            'order_remarks': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }
        field_order = ('parent_category', 'category', 'order_remarks')
