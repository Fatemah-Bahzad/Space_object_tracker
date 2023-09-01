from datetime import datetime, timezone
from client import TrackPlanet, TrackSatellite, TrackBodyT01, TrackBodyT21
import click


def print_views(object1,views):
    for i in views:
        return ("UTC Time: %s\nLocal Time: %s\nAzimuth: %f\nAltitude: %f\n"%(str(i['UTC Time'])[:19],str(i["Local Time"])[:19], i['az'].degrees, i['alt'].degrees))

def print_viewssat(views): #try to make this into one fit all 
    for i in views:
        return("UTC Time: %s\nLocal Time: %s\nAzimuth: %f\nAltitude: %f\n"%(str(i['UTC Time'])[:19],str(i["Local Time"])[:19], i['az'].degrees, i['alt'].degrees))

def validate_time(ctx, param, value):
    return value


def validate_planet(ctx, param, value):
    if value.lower().strip() not in ["sun",'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'neptune', 'uranus', "pluto", "moon"]:
        raise click.BadParameter(f"The planet provided ({value}) is not a valid planet. Please provide a valid planet.")
    else:
        return value



def get_planet_track(planet, latitude, longitude, points, angle,time_offset):
    planet_client = TrackPlanet(lat=latitude, lon=longitude, planet=planet)
    planet_views = planet_client.get_view(points=points,time_offset=time_offset)
    filtered_view = filter_for_elevation(planet_views, angle)
    #output=(print_views(planet,filtered_view))
    return filtered_view


def get_sat_track(norad_id, latitude, longitude, points, angle,sat,time_offset):
    sat_client = TrackSatellite(lat=latitude, lon=longitude, url=True, id1=norad_id,sat=sat)
    sat_views = sat_client.get_view(points=points,time_offset=time_offset)
    filtered_view = filter_for_elevation(sat_views, min_angle=angle)
#     return print_viewssat(filtered_view )
    return filtered_view


def get_voyager_track(latitude, longitude, points, angle,time_offset):
    voyager_client = TrackBodyT01(lat=latitude, lon=longitude)
    voyager_view = voyager_client.get_view(points=points,time_offset=time_offset)
    filtered_view = filter_for_elevation(views=voyager_view, min_angle=angle)
#     return print_views("Voyager 1",filtered_view)
    return filtered_view


@click.command('track_asteroid', short_help="Function to track the orbit of the Didymos asteroid.")
@click.option('--latitude', '--lat', required=True, default='', type=float, show_default=True,
              help="Latitude of the location from which you want to track.")
@click.option('--longitude', '--lon', required=True, default='', type=float, show_default=True,
              help="Longitude of the locaiton from which you want to track.")
@click.option('--initial_time', required=True, default='2022/05/01-00:00:00', type=str, show_default=True,
              help="Start time from which you'd like to observe the planetary track. Of the form YYYY/MM/DD-HH:MM:SS",
              callback=validate_time)
@click.option('--end_time', required=True, default='2022/05/2-00:00:00', type=str, show_default=True,
              help="End time for which you'd like to observe the planetary track till. Of the form YYYY/MM/DD-HH:MM:SS",
              callback=validate_time)
@click.option('--points', '-p', required=True, default=100, type=int, show_default=True,
              help="Number of samples to collect.")
@click.option('--angle', '-a', required=True, default=0, type=int, show_default=True, help="The minimum viewing angle.")
def get_asteroid_track(latitude, longitude, initial_time, end_time, points, angle):
    print(
        f'Body: 65803 Didymos\nInitial Time: {initial_time}\nEnd Time: {end_time}\n(Lat, Lon): ({latitude}, {longitude})\nPoints: {points}\nAngle: {angle}')
    initial_time = datetime.strptime(initial_time, '%Y/%m/%d-%H:%M:%S').replace(tzinfo=timezone.utc)
    end_time = datetime.strptime(end_time, '%Y/%m/%d-%H:%M:%S').replace(tzinfo=timezone.utc)
    asteroid_client = TrackBodyT21(lat=latitude, lon=longitude)
    asteroid_view = asteroid_client.get_view(time_start=initial_time, time_stop=end_time, points=points)
    filtered_view = filter_for_elevation(views=asteroid_view, min_angle=angle)
    print_views("i",filtered_view)


def filter_for_elevation(views, min_angle):
    o = []
    #print(views)
    if views['alt'].degrees >= min_angle:
        o.append(views)
    return o


@click.group()
def main():
    pass


#main.add_command(get_planet_track)
#main.add_command(get_sat_track)
main.add_command(get_asteroid_track)
#main.add_command(get_voyager_track)

if __name__ == '__main__':
    main()
