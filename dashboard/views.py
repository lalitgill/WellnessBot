from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Item
from .forms import ItemForm
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'dashboard/dashboard.html', {'items': items})

class AddItemView(View):
    def get(self, request):
        form = ItemForm()
        return render(request, 'dashboard/add_item.html', {'form': form})

    def post(self, request):
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return render(request, 'dashboard/add_item.html', {'form': form})

class DeleteItemView(View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return redirect('dashboard')