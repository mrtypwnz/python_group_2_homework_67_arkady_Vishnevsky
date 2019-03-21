from django.db import models
from django.urls import reverse
import random
import string
from django.conf import settings


class SoftDeleteManager(models.Manager):
    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)
    poster = models.ImageField(upload_to='posters', null=True, blank=True)
    release_date = models.DateField()
    finish_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', related_name='categories', blank=True)

    objects = SoftDeleteManager()

    def get_absolute_url(self):
        return reverse('api_v1:movie-detail', kwargs={'pk': self.pk})

    def get_categories_display(self):
        return self.categories.all()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Hall(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(Hall, related_name='seats', on_delete=models.PROTECT)
    row = models.CharField(max_length=10)
    seat = models.CharField(max_length=5)

    def __str__(self):
        return "Row %s Seat %s" % (self.row, self.seat)


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='shows')
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, related_name='shows')
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "%s, %s (%s - %s)" % (self.movie, self.hall,
                                     self.starts_at.strftime('%d.%m.%Y %H:%M'),
                                     self.ends_at.strftime('%d.%m.%Y %H:%M'))


def generate_code():
    code = ""
    for i in range(0, settings.BOOKING_CODE_LENGTH):
        code += random.choice(string.digits)
    return code


BOOKING_STATUS_CHOICES = [
    ('created', 'Created'),
    ('sold', 'Sold'),
    ('canceled', 'Canceled'),
]


class Book(models.Model):
    # значение по умолчанию - метод generate_code, который генерирует случайный код из 6 цифр
    # свойство unique_for_date делает это поле уникальным в пределах даты, указанной в поле created_at
    code = models.CharField(max_length=10, unique_for_date='created_at', default=generate_code, editable=False)
    show = models.ForeignKey(Show, on_delete=models.PROTECT, related_name='booking')
    seats = models.ManyToManyField(Seat, related_name='booking')
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.show, self.code)

    def get_seats_display(self):
        seats = ""
        for seat in self.seats.all():
            seats += "R%sS%s " % (seat.row, seat.seat)
        return seats.rstrip()

class Discount(models.Model):
    name = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    discount_from = models.DateTimeField()
    discount_to = models.DateTimeField()

class Ticket(models.Model):
    show = models.ForeignKey(Show, related_name='ticket_show', on_delete=models.PROTECT)
    seat = models.ForeignKey(Seat, related_name='ticket_seat', on_delete=models.PROTECT)
    discount = models.ForeignKey(Discount, related_name='ticket_discount', on_delete=models.PROTECT)
    return_ticket = models.BooleanField(default='False')