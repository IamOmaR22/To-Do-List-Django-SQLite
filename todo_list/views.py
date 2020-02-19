from django.shortcuts import render,redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView # for signup form view
from django.contrib.auth.forms import UserCreationForm  # for signup form
# from django.contrib.auth.mixins import LoginRequiredMixin # its only for class base view.individiual user can acces their todo only
from django.contrib.auth.decorators import login_required # without login user can not see home page
from django.urls import reverse_lazy
from django.contrib.auth import logout ## For Log Out


# Create your views here.
@login_required  # it will work after login.
def home(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)
        if form.is_valid():
            form.save()
            all_items = List.objects.all  # List is class name
            messages.success(request, ('Item Has Been Added To List!'))
            return render(request, 'home.html', {'all_items':all_items})
    else:
        all_items = List.objects.all  # List is class name
        return render(request, 'home.html', {'all_items':all_items})

    # def get_queryset(self):
    #     todo_list = super().get_queryset()
    #     return todo_list.filter(List = self.request.user)

@login_required
def about(request):
    context = {'first_name':'OmaR','last_name':'FaruK'}
    return render(request, 'about.html', context)

def delete(request,list_id):
    item = List.objects.get(pk=list_id)
    item.delete()
    messages.success(request, ('Item Has Been Deleted!'))
    return redirect('home')

def cross_off(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('home')

def uncross(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('home')

def edit(request, list_id):
    if request.method == 'POST':
        item = List.objects.get(pk=list_id)
        form = ListForm(request.POST or None, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, ('Item Has Been Edited!'))
            return redirect('home') # to go other page
    else:
        item = List.objects.get(pk=list_id)
        return render(request, 'edit.html', {'item':item})

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')


##-## Log Out Start ##-##
def logout_view(request):
    logout(request)
    return redirect('login')
##-## Log Out Start ##-##