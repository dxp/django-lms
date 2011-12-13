from django import forms

from tinymce.widgets import TinyMCE
from libs.widgets import ShortNameClearableFileInput

class ProfileForm(forms.Form):
    mugshot = forms.FileField(label = 'Profile image', required = False, widget=ShortNameClearableFileInput)
    resume = forms.FileField(label = 'Resume', required = False, widget=ShortNameClearableFileInput)
    biography = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    def save(self, profile):
        profile.mugshot = self.cleaned_data['mugshot']
        profile.resume = self.cleaned_data['resume']

        profile.data['biography'] = self.cleaned_data['biography']
        profile.save()
