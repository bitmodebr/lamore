from django.db import models
import uuid


class Client(models.Model):
    class LensType(models.TextChoices):
        MULTIFOCAL_POLI = 'mp', 'Multifocal - Policarbonato'
        MULTIFOCAL_ORGA = 'mo', 'Multifocal - Orgânica'
        MULTIFOCAL_CRIS = 'mc', 'Multifocal - Cristal'
        SIMPLE_VIEW_POLI = 'sp', 'Visão Simples - Policarbonato'
        SIMPLE_VIEW_ORGA = 'so', 'Visão Simples - Orgânica'
        SIMPLE_VIEW_CRIS = 'sc', 'Visão Simples - Cristal'


    id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    first_name = models.CharField('nome', max_length=30)
    last_name = models.CharField('sobrenome', max_length=100, blank=True)
    phone = models.CharField('fone', max_length=15, blank=True)
    lens_type = models.CharField('tipo de lente', max_length=2, choices=LensType.choices, blank=True)
    entry_date = models.DateField('data de entrada', null=True, blank=True)
    delivery_date = models.DateField('data de entrega', null=True, blank=True)
    register_date = models.DateTimeField('data de cadastro', auto_now_add=True, editable=False)
    frame_type = models.CharField('tipo de armação', max_length=50, blank=True)
    last_purchase = models.DateField('ultima compra', null=True, blank=True)
    birthday = models.DateField('aniversario', null=True, blank=True)

    def __str__(self) -> str:
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.first_name
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = "Clientes"


class Prescription(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    doctor_name = models.CharField('nome do médico', max_length=100)
    issued_at = models.DateField('data da receita')
    valid_until = models.DateField('válido até', null=True, blank=True)
    far_right = models.DecimalField('Longe - Direito', max_digits=5, decimal_places=2, null=True, blank=True)
    far_left = models.DecimalField('Longe - Esquerdo', max_digits=5, decimal_places=2, null=True, blank=True)
    near_right = models.DecimalField('Perto - Direito', max_digits=5, decimal_places=2, null=True, blank=True)
    near_left = models.DecimalField('Perto - Esquerdo', max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Receita de {self.client} - {self.issued_at}'

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"


class EyePrescriptionMeasurement(models.Model):
    prescription = models.OneToOneField(
        Prescription,
        on_delete=models.CASCADE,
        related_name='measurements'
    )
    axis_right = models.DecimalField('Eixo - Direito', max_digits=5, decimal_places=2, null=True, blank=True)
    dnp_right = models.DecimalField('Distância Noso Pupilas - Direito', max_digits=5, decimal_places=2, null=True, blank=True)
    height_right = models.DecimalField('Altura - Direito', max_digits=5, decimal_places=2, null=True, blank=True)
    axis_left = models.DecimalField('Eixo - Esquerdo', max_digits=5, decimal_places=2, null=True, blank=True)
    dnp_left = models.DecimalField('Distância Noso Pupilas - Esquerdo', max_digits=5, decimal_places=2, null=True, blank=True)
    height_left = models.DecimalField('Altura - Esquerdo', max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Medida da Receita"
        verbose_name_plural = "Medidas das Receitas"

    def __str__(self):
        return f'Medida de {self.prescription.client} - {self.prescription.issued_at}'
