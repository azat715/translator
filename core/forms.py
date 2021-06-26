from django import forms


class TestForm(forms.Form):
    text_param = forms.CharField(label="Текстовый параметр", max_length=10)
    numeric_param = forms.IntegerField(label="Числовой параметр", max_value=5)
