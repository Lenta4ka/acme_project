from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user 

class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10
    
class BirthdayDetailView(DetailView):
    model = Birthday 
    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context 
    
class BirthdayCreateView(CreateView, LoginRequiredMixin):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form) 

class BirthdayUpdateView(UpdateView, OnlyAuthorMixin):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView, LoginRequiredMixin, OnlyAuthorMixin):
    model = Birthday
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context 