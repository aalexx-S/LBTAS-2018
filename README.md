# PTT Reply Location Marker

This program use some geolocation tech to find PTT replyers' location.

## Usage

```
python3 findLocation.py [-h] [-k KEYFILE] [-db DATABASE] [-shp SHAPEFILE] [-qt QUERYTIMES] [-o OUTPUT | -silent] INPUT
```

Use -h for more details.

### Key File

Users need to place the api services they want to use and other required information in a file. By default, its called "key.txt", but can be changed via '-k'.

Each line contains a service, formatted as follow:

```
SERVICE_NAME [other required information when making requests, like key]
```

I will assume you are using a free trial of all the api, so there will be limitation on each api service. Also, all limitations are hard coded, so if the services change their limits...

Supported services:

* [ipapi](http://ip-api.com/) - 150 requests / min
	```
	ipapi
	```

* [geoplugin](https://www.geoplugin.com/) - 2 requests / second 
	```
	geoplugin
	```

### Input

Input is a web ptt post url. For example: [Gossiping Board November 2018 Chat](https://www.ptt.cc/bbs/Gossiping/M.1541093112.A.727.html) page.

## Dependency

### Python3 Packages

These packages cab be installed through pip3.

* [pandas](https://pandas.pydata.org/) - Reading and parsing csv file and put into sqlite.

* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web scraping.

* [fiona](https://github.com/Toblerity/Fiona) - Read shapefile.

* [shapely](https://pypi.org/project/Shapely/) - Administration area matching.

### Taiwan Administration Area Shapefile

User has to provide the shapefile of Taiwan administration area. The shapefile can be found on the [Taiwan government open data platform](https://data.gov.tw/datasets/search?qs=%E7%9B%B4%E8%BD%84%E5%B8%82%E3%80%81%E7%B8%A3%E5%B8%82%E7%95%8C%E7%B7%9A). Choose the download with SHP file. Extract all the files and place them together.

By default, the shapefile is called "./shp/COUNTY\_MOI\_1070516.shp", but this can be changed with optional arguments '-shp' by passing the filename of the .shp file.

If -shp option is used, the program will automatically handle the path to all the other files.

### IP2Location Database

User should place [IP2Location database](https://lite.ip2location.com/) in the project for faster performance.

All it does is filter the ip that is not in Taiwan.

The database must also include longitude and latitude information.

Please download the CSV one since I don't know what that bin file is.

This site or product includes IP2Location LITE data available from [http://www.ip2location.com](http://www.ip2location.com).
