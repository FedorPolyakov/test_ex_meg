from django import forms
from .models import PostNumber


class PostNumberForm(forms.ModelForm):

    class Meta:
        model = PostNumber
        fields = ['number_int', 'nds', 'nds_percent']


    def clean_number_int(self):
        required_symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', ' ']
        data = self.cleaned_data['number_int']
        for x in data:
            if x not in required_symbols:
                raise forms.ValidationError(f'Недопустимые символы!'
                                            f'Допустимы только цифры, пробел, одна точка или запятая')
        if data.count(',') > 1:
            raise forms.ValidationError(f'Допусима только одна запятая в поле ввода. У вас их {data.count(",")}')
        elif data.count('.') > 1:
            raise forms.ValidationError(f'Допусима только одна точка в поле ввода. У вас их {data.count(".")}')
        if data[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            raise forms.ValidationError(f'Число должны начинаться с цифры')
        for x in data:
            if x == ',':
                x = '.'
        return data

    def clean_nds_percent(self):
        nds = self.cleaned_data['nds']
        data = self.cleaned_data['nds_percent']
        print(nds)
        if nds == True:
            if data == 0:
                nds = False
                return nds
            if data < 0 or data > 100:
                raise forms.ValidationError('Процент НДС не может быть больше 100 или меньше 0')
            return data
        else:
            return data


