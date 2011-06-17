class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Course
        fields = ('private',)
