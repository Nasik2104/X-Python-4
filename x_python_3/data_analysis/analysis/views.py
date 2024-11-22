from django.views.generic import ListView, CreateView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd


from .helpers import Analyzer
from .forms import AddFileForm
from .models import FileStorage, History

class Index(LoginRequiredMixin, CreateView):
    form_class = AddFileForm
    template_name = 'analysis/index.html'
    success_url = reverse_lazy('user:user-profile')

    def form_valid(self, form):
        print(1)
        form.instance.user = self.request.user
        return super().form_valid(form)


class CSVAnalysis(ListView):
    paginate_by = 50
    template_name = 'analysis/csv_analysis.html'
    context_object_name = 'data'

    def get_queryset(self):
        file_id = self.request.GET.get("file_id")
        if file_id:
            file = FileStorage.objects.get(id=int(file_id))
        else:
            raise ValueError

        self.analyzer = Analyzer(file_path=file.file.path)
        self.analyzer.load_data()

        column = self.request.GET.get('column')
        condition = self.request.GET.get('condition')
        value = self.request.GET.get('value')
        column_2 = self.request.GET.get('column_2')
        search = self.request.GET.get('search')

        history_data = {
            'file': file,
            'user': self.request.user,
        }

        if value and column and condition:
            try:
                self.analyzer.filter_data(column, condition, float(value))
                history_data.update({'column': column, 'condition': condition, 'value': value})
            except:
                messages.error(self.request, "Enter correct data")

        if column_2 and search:
            try:
                condition = '=='
                self.analyzer.filter_data(column_2, condition, str(search))
                history_data.update({'column_2': column_2, 'search': search})
            except:
                messages.error(self.request, "Enter correct data")

        if history_data.get('column') or history_data.get('column_2'):
            History.objects.create(**history_data)

        return self.analyzer.data.to_dict('records')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['statistics'] = {}
        context['rows'] = len(self.analyzer.data)

        for column in self.analyzer.data.columns:
            if pd.api.types.is_numeric_dtype(self.analyzer.data[column]):
                statistics = self.analyzer.calculate_statistics(column)
                context['statistics'][column] = statistics

        return context
