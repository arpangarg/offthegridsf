from datetime import datetime, timedelta
from requests import get
from json import loads
import operator
from foodtrucks.models import Truck, TruckFrequency


ACCESS_TOKEN = '1424219667820757|4ae4cf886bc70d3a9d9a87dc70d90fd7'

GRAPH_URL_OVERVIEW = (
	'https://graph.facebook.com/OffTheGridSF/events?access_token={0}&limit=100'
)

GRAPH_URL_DETAIL = 'https://graph.facebook.com/{0}?access_token={1}'

def get_event_overviews():
	response = get(GRAPH_URL_OVERVIEW.format(ACCESS_TOKEN))
	return loads(response.content)['data']

def db_get_most_recent():
	most_rec = Truck.objects.order_by('-start_time')
	if most_rec:
		return most_rec[0]
	else:
		return None

def get_detailed_event(graph_id):
	response = get(GRAPH_URL_DETAIL.format(graph_id, ACCESS_TOKEN))
	detailed_data = loads(response.content)

	search_through = detailed_data['description'].strip().split('\n')

	vendor_start = None
	for component in search_through:
		if 'vendors:' in component.lower():
			vendor_start = search_through.index(component) + 1
			break

	vendor_list = []
	if vendor_start:
		for vendor in search_through[vendor_start:]:
			if vendor.strip() != '':
				vendor_list.append(vendor.strip().split('(')[0].strip())
			else:
				break

	try:
		truck_data = {
			'graph_id': detailed_data['id'].strip(),
			'start_time': datetime.strptime(
				detailed_data['start_time'].strip(),
				'%Y-%m-%dT%H:%M:%S+0000'
			) - timedelta(hours=8),
			'end_time': datetime.strptime(
				detailed_data['end_time'].strip(),
				'%Y-%m-%dT%H:%M:%S+0000'
			) - timedelta(hours=8),
			'location': detailed_data['location'].strip(),
			'vendor_list': vendor_list
		}
	except ValueError:
		return None

	return truck_data

def insert_event(truck_data):
	if truck_data:
		for vendor in truck_data['vendor_list']:
			truck = Truck(
				graph_id = truck_data['graph_id'],
				vendor = vendor,
				start_time = truck_data['start_time'],
				end_time = truck_data['end_time'],
				location = truck_data['location']
			)

			truck.save()

def get_data():
	event_overviews = get_event_overviews()
	most_recent = db_get_most_recent()

	for overview in event_overviews:
		if most_recent and overview['id'] == most_recent.graph_id:
			break
		truck_data = get_detailed_event(overview['id'])
		insert_event(truck_data)

def get_last_30_days():
	return Truck.objects.filter(
		start_time__lte = datetime.today(),
		start_time__gte = datetime.today() - timedelta(days=30)
	)


def update_frequencies():
	trucks = get_last_30_days()
	vendor_list = [truck.vendor for truck in trucks]

	unique_vendors = list(set(vendor_list))
	freq = {}

	for vendor in unique_vendors:
		freq[vendor] = vendor_list.count(vendor)

	freq_sorted = sorted(
		freq.iteritems(),
		key=operator.itemgetter(1),
		reverse=True
	)

	TruckFrequency.objects.all().delete()

	for truck, freq in freq_sorted:
		truck_freq = TruckFrequency(vendor=truck, frequency=freq)
		truck_freq.save()

if __name__ == "__main__":

	get_data()

	update_frequencies()
