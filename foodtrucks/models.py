from django.db import models


class Truck(models.Model):
	graph_id = models.CharField(max_length=20)
	vendor = models.CharField(max_length=50)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	location = models.CharField(max_length=100)


class TruckFrequency(models.Model):
	vendor = models.CharField(max_length=50)
	frequency = models.IntegerField()
