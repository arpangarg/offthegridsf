from django.shortcuts import render
from models import TruckFrequency


def display_page(request):
	vendor_list = TruckFrequency.objects.all()

	return render(request, 'index.html', {'vendor_list': vendor_list})
