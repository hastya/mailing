from django.db import models
from django.utils import timezone

import users.models

NULLABLE = {'blank': True, 'null': True}

STATUS_CHOICES = [
    ('start', 'start'),
    ('finish', 'finish'),
    ('created', 'created'),
]
INTERVAL_CHOICES = [
    ('once_a_day', 'once_a_day'),
    ('once_a_week', 'once_a_week'),
    ('once_a_month', 'once_a_month'),
]


class Client(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Контактный email')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    def __repr__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Тело письма')
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец сообщения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название рассылки')
    client = models.ManyToManyField(Client, verbose_name='Кому')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Время старта рассылки')
    next_date = models.DateTimeField(default=timezone.now, verbose_name='Время следующей рассылки')
    end_date = models.DateTimeField(verbose_name='Время окончания рассылки')
    interval = models.CharField(default='Разовая', max_length=50, choices=INTERVAL_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, help_text="Выберите Создана или Завершена")
    is_activated = models.BooleanField(default=True, verbose_name='Действующая')
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец рассылки')

    def __str__(self):
        return f'"{self.name}"'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('start_date',)

        permissions = [
            ('set_is_activated', 'Может отключать рассылку')
        ]


class Logs(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    last_mailing_time = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=50, verbose_name='Статус попытки', null=True)
    response = models.CharField(max_length=200, verbose_name="Ответ почтового сервера", **NULLABLE)

    def __str__(self):
        return f'Отправлено: {self.last_mailing_time}, ' \
               f'Статус: {self.status}'

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'
