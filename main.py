import csv
from typing import List, Any

from meteofrance_api import MeteoFranceClient
from meteofrance_api.helpers import readeable_phenomenoms_dict


def weather(city: str, day: int) -> list[Any]:
    # Init client
    client = MeteoFranceClient()
    print(city)
    # Search a location from name.
    list_places = client.search_places(city)
    if list_places:
        my_place = list_places[0]

        # Fetch weather forecast for the location
        my_place_weather_forecast = client.get_forecast_for_place(my_place)

        # Get the daily forecast
        my_place_daily_forecast = my_place_weather_forecast.daily_forecast
        return [my_place_daily_forecast[day]['weather12H']['desc'], my_place_daily_forecast[day]['T']['min'],
                my_place_daily_forecast[day]['T']['max']]
    else:
        return ["no value", "no value", "no value", ]


def read_csv(name: str) -> list:
    f = open(name)
    myReader = csv.reader(f)
    result = []
    for row in myReader:
        result.append(row)
    return result


def list_weather(list_de_station: list, day: int) -> list:
    prediction_list = []
    for station in list_de_station:
        prediction_list.append(weather(station[0], day))
    return prediction_list


def write_csv(list_weather_resorts):
    with open('balneaire_result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list_weather_resorts)


if __name__ == '__main__':
    listStation = read_csv("balneaire.csv")
    day = input("saississer le jour(aujourd'hui:0,demain:1,...)")
    list_weather_resort = list_weather(listStation, int(day))
    print(list_weather_resort)
    list_station_final = []
    cpt = 0
    for i in listStation:
        list_station_final.append([i, list_weather_resort[cpt][0], list_weather_resort[cpt][1], list_weather_resort[cpt][2]])
        cpt+=1
    write_csv(list_station_final)
