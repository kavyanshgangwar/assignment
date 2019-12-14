from django.shortcuts import render
from .models import MyModel
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import MyModelForm
from django.core.files import File
from .encrypt import encrypt
import os
# Create your views here.

# index view 
# this view is making the homepage of the app
def index(request):
    # creating a list of models ordered by filename and sending them to template
    mymodels = MyModel.objects.order_by('myfilename')
    context = {'mymodels':mymodels}
    return render(request,'asignments/index.html',context)

# create view
# this view is used for making new entries in the database
def create(request):

    if(request.method == 'POST'):
        
        # using model form to handel the file upload
        form = MyModelForm(request.POST , request.FILES)
        if form.is_valid:
            
            #creating a model instance to handel the encryption process before creating the entry
            m1 = MyModel()

            # the handle_upload_file function is used to handel the file uploaded and the encryption of file data
            m1.myencryption = handle_uploaded_file(request.POST['myfilename'],request.FILES['myfile'])
            
            m1.myfilename = request.POST['myfilename']
            m1.myfile = File(open('asignments/uploads/'+ request.POST['myfilename'],'r'))
            m1.save()
            os.remove('asignments/uploads/' + request.POST['myfilename'])
            
            # redirecting to homepage
            return HttpResponseRedirect(reverse('assignments:index'))
    
    # rendering the create page
    return render(request,'asignments/create.html')

# definig a view to update the content of the file
# this function uses html form to get content of updated file
def update(request, model_id):
    # getting the model we want to update content of
    model = MyModel.objects.get(id = model_id)
    
    data = ""
    with open(model.myfile.path,'r') as f:
        data = data + f.read()

    if request.method == 'POST':
        # updating the content of the file
        with open(model.myfile.path,'w') as f:
            f.write(request.POST["content"])

        # updating the content of the file into the database
        # the overriden update function will take care of the encryption value related to file
        MyModel.objects.filter(id = model_id).update(myfile = model.myfile)

        # redirecting to the homepage
        return HttpResponseRedirect(reverse('assignments:index'))

    # sending the initial data of the file as well as the model instance to template to edit the data of file    
    context = {'data':data,'model':model}

    # rendering the html page
    return render(request,'asignments/update.html',context)
        
# function to handel upload of the file
# n is the name of the file
# f is the request.FILES 
def handle_uploaded_file(n,f):

    # saving the data bytes of the file into the file 
    with open('asignments/uploads/' + n, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # reading the data to get encrypted value of the file content
    with open('asignments/uploads/' + n, 'r') as destination:
        data = destination.read()

    # returning the encrypted data
    return encrypt(data)
