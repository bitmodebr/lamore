from django.db import models


class Client(models.Model):
    # campos atuais...
    pass


class Doctor(models.Model):
    name = models.CharField('nome', max_length=100)
    crm = models.CharField('CRM', max_length=30, blank=True)
    specialty = models.CharField('especialidade', max_length=80, blank=True)

    def __str__(self):
        return self.name


class EyeSide(models.TextChoices):
    LEFT = 'L', 'Olho esquerdo'
    RIGHT = 'R', 'Olho direito'


class DistanceType(models.TextChoices):
    FAR = 'F', 'Longe'
    NEAR = 'N', 'Perto'


class Prescription(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name='prescriptions'
    )
    issued_at = models.DateField('data da receita')
    valid_until = models.DateField('válido até', null=True, blank=True)
    notes = models.TextField('observações', blank=True)

    def __str__(self):
        return f'Receita de {self.client} - {self.issued_at}'


class EyePrescriptionMeasurement(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='measurements'
    )
    side = models.CharField(max_length=1, choices=EyeSide.choices)
    distance_type = models.CharField(max_length=1, choices=DistanceType.choices)
    sphere = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cylinder = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    axis = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
    dnp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('prescription', 'side', 'distance_type')


'''
from django.db import models


class Client(models.Model):
    class LensType(models.TextChoices):
        MULTIFOCAL = 'm', 'Multifocal'
        SIMPLE_VIEW = 's', 'Visão Simples'

    first_name = models.CharField('nome', max_length=30)
    last_name = models.CharField('sobrenome', max_length=100, blank=True)
    phone = models.CharField('fone', max_length=15, blank=True)
    lens_type = models.CharField('tipo de lente', max_length=1, choices=LensType.choices, blank=True)
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


class EyeSide(models.TextChoices):
    LEFT = 'L', 'Olho esquerdo'
    RIGHT = 'R', 'Olho direito'


class EyeMeasurement(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='eye_measurements'
    )
    side = models.CharField(max_length=1, choices=EyeSide.choices)
    axis = models.DecimalField(max_digits=6, decimal_places=2)
    dnp = models.DecimalField(max_digits=6, decimal_places=2) # distância noso pupilar
    height = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('client', 'side')

'''