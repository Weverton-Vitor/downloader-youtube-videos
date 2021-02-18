from django import forms

class DownloaderYoutubeForm(forms.Form):
    link = forms.CharField(required=True, error_messages={'required':'Campo Obrigatório'})