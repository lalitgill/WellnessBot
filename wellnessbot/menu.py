from django.urls import reverse
from django.utils.translation import gettext_lazy as _

def menu_items(request):
    return [
        {
            'name': 'Home',
            'url': reverse('admin:index'),
            'icon': 'fas fa-tachometer-alt',
        },
        {
            'name': 'Dashboard',
            'url': reverse('dashboard'),
            'icon': 'fas fa-chart-bar',
        },
        {
            'name': 'Add Item',
            'url': reverse('add_item'),
            'icon': 'fas fa-plus',
        },
    ]