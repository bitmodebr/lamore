from django.contrib import admin

from client.models import Client, Prescription, EyePrescriptionMeasurement

import random

import string


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['reduced_id', 'first_name', 'last_name', 'entry_date', 'register_date']
    ordering = ['first_name']
    search_fields = ['first_name']
    list_per_page = 25

    def reduced_id(self, obj):
        return str(obj.id)[:5]


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['pseudo_id', 'client', 'doctor_name', 'issued_at', 'valid_until']
    list_editable = ['doctor_name']
    ordering = ['client__first_name']
    search_fields = ['client__first_name', 'doctor_name']

    def pseudo_id(self, obj):
        random_string = ''.join(random.choices(string.ascii_lowercase, k=4))
        return f'{str(obj.id)}{random_string}'[:5]


@admin.register(EyePrescriptionMeasurement)
class EyePrescriptionMeasurementAdmin(admin.ModelAdmin):
    list_display = ['pseudo_id', 'prescription']
    ordering = ['prescription__client__first_name']
    search_fields = ['prescription__client__first_name']

    def pseudo_id(self, obj):
        random_string = ''.join(random.choices(string.ascii_lowercase, k=4))
        return f'{str(obj.id)}{random_string}'[:5]
