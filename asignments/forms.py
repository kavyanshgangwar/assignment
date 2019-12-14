from django import forms

# created a form for MyModel 
class MyModelForm(forms.Form):
    myfilename = forms.CharField(max_length = 200)
    myfile = forms.FileField()