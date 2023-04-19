from django.shortcuts import render
from django.http import JsonResponse
import folium
from static.com import messages
import json
import os


# Create your views here.
def index(request):
    return render(request, 'index.html')

def is_point_in_path(x: float, y: float, poly) -> bool:
    num = len(poly)
    j = num - 1
    c = False
    for i in range(num):
        if (x == poly[i][0]) and (y == poly[i][1]):
            return True
        if ((poly[i][1] > y) != (poly[j][1] > y)):
            slope = (x - poly[i][0]) * (poly[j][1] - poly[i][1]) - (poly[j][0] - poly[i][0]) * (y - poly[i][1])
            if slope == 0:
                return True
            if (slope < 0) != (poly[j][1] < poly[i][1]):
                c = not c
        j = i
    return c

def map(request):
    p1=[
        (52.25668206898288,104.26340472198405),(52.25817582347088,104.27125256195853),
        (52.25873596843354,104.27128029284205),(52.25924518498766,104.27247272082326),
        (52.261638424473404,104.27128029284205),(52.26471040783642,104.26753662359545),
        (52.26416731024287,104.25943920567232),(52.25668206898288,104.26340472198405)]
    l1=[
        (52.26257598220359, 104.2612796025416),
        (52.26253294468879, 104.2610934846107),
        (52.26243399758629, 104.26111761581647),
        (52.26245767432858, 104.26126531729943),
        (52.26232636007098, 104.26131803014349),
        (52.26218585510812, 104.26143726867795),
        (52.262161650182165, 104.2615570252868),
        (52.262219283628525, 104.26181530526208),
        (52.26235461300167, 104.26264454545743),
        (52.262536160383306, 104.26331314462969),
        (52.2627531633811, 104.26431191523271),
        (52.26280675073904, 104.26459984462589),
        (52.262615035480366, 104.26481418110352),
        (52.2626327278901, 104.26495081316575)]

    coordinate = l1[-1]
    marker1 = [52.2573, 104.2652]
    # Create map
    m = folium.Map(location=[52.257529268365516, 104.26505193126633], zoom_start=15)
    m.get_root().html.add_child(folium.Element('<style>.leaflet-control-attribution {display:none;}</style>')) # type: ignore

    shapesLayer = folium.FeatureGroup(name="warning").add_to(m)

    poin=is_point_in_path(marker1[0], marker1[1], p1)
    
    if not poin:
        color_p1="red"
    else:
        color_p1 = "green"

    folium.Polygon(
        p1,
        weight=2,
        fill_color=color_p1,
        fill_opacity=0.2).add_to(shapesLayer)


    shapesLayer = folium.FeatureGroup(name="warning").add_to(m)


    # Map layers
    # folium.raster_layers.TileLayer("OpenStreetMap").add_to(m)
    # folium.raster_layers.TileLayer("Stamen Terrain").add_to(m)
    # folium.raster_layers.TileLayer("Stamen Toner").add_to(m)
    # folium.raster_layers.TileLayer("CartoDB positron").add_to(m)

    # folium.LayerControl().add_to(m)

    #Create markers
    tooltip = "Click me!"
    
    folium.Marker(location=marker1, popup="<i>Backend dev</i>",
             tooltip=tooltip).add_to(m)
    
    
    # Задаем координаты точек маршрута
    # route = [[52.2574, 104.2648], [52.2578, 104.2643], [52.2576, 104.2636], [52.2601, 104.2623], [52.2600, 104.2617],
    #      [52.2607, 104.2614], [52.2607, 104.2614], [52.2612, 104.2641], [52.2625, 104.2634], [52.2626, 104.2633],
    #      [52.2627, 104.2643]]
    # points = [route]

    # # Создаем объект ломаной линии и добавляем его на карту
    # folium.PolyLine(points, color='red', weight=2).add_to(m)


    # m.attributionControl.setPrefix(False)

    # Get html represantation of map
    m = m._repr_html_()
    
    context = {
        'm': m
    }
    return render(request, 'map.html', context)


def chat(request):
    data = {'message': messages,
            }
    return JsonResponse(data)






def send_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message', '')
        print(user_message)
        f = open("C:/code/gps_project/message.txt", "a")
        f.write(user_message + '\n')
        f.close()
        # Здесь можно выполнить какие-то действия с полученным сообщением
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

