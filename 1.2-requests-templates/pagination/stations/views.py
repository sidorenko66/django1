from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

import csv
from pagination.settings import BUS_STATION_CSV

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    bus_stations = []
    with open(BUS_STATION_CSV,encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bus_stations.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(bus_stations, 10)
    page = paginator.get_page(page_number)
    context = {
         #'bus_stations': bus_stations[page.number*10 - 10 : page.number*10],
         'page': page,
    }
    return render(request, 'stations/index.html', context)
