from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from django.core import validators


class Store(models.Model):
    name = models.CharField('部門', max_length=100)
    address = models.CharField('住所', max_length=100, null=True, blank=True)
    tel = models.CharField('電話番号', max_length=100, null=True, blank=True)
    description = models.TextField('説明', default="", blank=True)
    image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name='スタッフ', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, verbose_name='部門', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store}：{self.user}'


class Modality(models.Model):
    name = models.CharField('検査機器', max_length=100)
    store = models.ForeignKey(Store, verbose_name='部門', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True)

    def __str__(self):
        return f'{self.store}：{self.name}'


class Patient(models.Model):
    pt_id = models.IntegerField(
        'ID',
        null=False,
        blank=False,
        unique=False,
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(1000000)]
    )
    pt_name = models.CharField(verbose_name='患者名', max_length=20, null=False, blank=False)
    pt_gender = models.CharField('性別', max_length=5, null=True, blank=True)
    pt_birthday = models.DateField('誕生日', null=True, blank=True)
    pt_remarks = models.TextField('備考', default="", null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'ID:{self.pt_id} NAME:{self.pt_name}'


class ParentCategory(models.Model):
    name = models.CharField('親カテゴリ名', max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=255)
    parent = models.ForeignKey(ParentCategory, verbose_name='親カテゴリ', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Remark(models.Model):
    order_remarks = models.CharField('備考', max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT, null=True, blank=True)
    parts = models.CharField('検査部位', max_length=255, null=True, blank=True)

    def __str__(self):
        return f'部位:{self.category} 検査部位:{self.parts} 備考:{self.order_remarks}'


class Booking(models.Model):
    staff = models.ForeignKey(Staff, verbose_name='スタッフ', on_delete=models.CASCADE, null=True, blank=True)
    modality = models.ForeignKey(Modality, verbose_name='モダリティ', on_delete=models.CASCADE, null=True, blank=True)
    pt_data = models.ForeignKey(
        Patient,
        verbose_name='患者データ',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="pt_data"
    )
    start = models.DateTimeField('開始時間', default=timezone.now, null=True, blank=True)
    end = models.DateTimeField('終了時間', default=timezone.now, null=True, blank=True)
    date = models.DateField('日付', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    orders = models.OneToOneField(
        Remark,
        verbose_name='備考',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M')
        # created_at = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.pt_data} {start} ~ {end} {self.staff}{self.modality}{self.orders}{self.created_at}'



