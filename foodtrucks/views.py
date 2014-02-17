from django.shortcuts import render
from models import TruckFrequency


def display_page(request):
	vendor_list = TruckFrequency.objects.all()
	#vendor_list = {}
	#for truck in truck_list:
	#	vendor_list[truck.vendor] = truck.frequency
	return render(request, 'index.html', {'vendor_list': vendor_list})
