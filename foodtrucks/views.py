from django.shortcuts import render
from models import TruckFrequency, TruckProperties


def display_page(request):
	truck_list = TruckFrequency.objects.all()

	popular_trucks = []
	max_freq = truck_list[0].frequency

	#This could be implemented much better with relationships rather than running a
	#query on the database each time.
	for truck in truck_list:
		try:
			truckP = TruckProperties.objects.get(vendor=truck.vendor)
			popular_trucks.append({
				'vendor': truck.vendor,
				'frequency': truck.frequency,
				'url': truckP.url,
				'img_url': truckP.img_url,
				'food_types': truckP.food_types,
				'popularity': str(100*truck.frequency / max_freq) + ' %'
			})

		except TruckProperties.DoesNotExist:
			continue

	return render(request, 'index.html', {'popular_trucks': popular_trucks})

def show_diagrams(request, diagram):
	if (diagram == '360pi_crawl'):
		return render(request, 'show_diagram.html', {'img_src': '360pi_crawl.png'})
	elif (diagram == 'amazon_reviews'):
		return render(request, 'show_diagram.html', {'img_src': 'amazon_reviews.png'})
	else:
		return display_page(request)
