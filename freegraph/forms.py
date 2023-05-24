from django import forms
import csv

class DadosCSVForm(forms.Form):
    csv_file = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(self.cleaned_data['csv_file'].name, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader)
            for coluna in header:
                self.fields[coluna] = forms.BooleanField(required=False)