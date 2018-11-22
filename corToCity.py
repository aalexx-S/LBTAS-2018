import fiona
import copy
from shapely.geometry import shape, Point
from pyproj import Proj, transform

config = None

def cor_to_city(all_queries):
    # read shapefile
    print("[Log] Constructing city shape.", file = config.stderr)
    ad_area_shp = fiona.open(config.shppath + '/' + config.shpname + '.shp', encoding = 'utf-8')
    shapes = {}
    attr = {}
    for area in ad_area_shp:
        city_id = int(area['properties']['COUNTYCODE'])
        shapes[city_id] = shape(area['geometry'])
        attr[city_id] = area['properties']

    # search location for each push and poster
    re = []
    for query in all_queries:
        # transfer to TWD97
        tmp = copy.deepcopy(query)
        # find matching shape, return the first one found. Whatever.
        for city, sh in shapes.items():
            if sh.contains(Point(tmp['longitude'], tmp['latitude'])):
                tmp['city'] = attr[city]['COUNTYNAME']
                break
        re.append(tmp)
    return re

# transfet longitude and latitude(EPAG4326) to TWD97(EPSG3826)
def trans(lon, lat):
    inp = Proj(init='epsg:4326')
    oup = Proj(init='epsg:3826')
    return transform(inp, oup, lon, lat)

