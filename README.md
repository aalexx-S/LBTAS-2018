# PTT Reply Location Marker

This program use some geolocation tech to find PTT replyers' location.

## Usage

Get the ptt post, and draw the statistic to a pie chart.
```
python3 genReplyPieChart.py INPUT
```
Note that this method does not provide any way to change any config because I am lazy and sick. Maybe I will add the options later when I feel better. I don't think its needed though.
You can make your own drawing/plotting functions easily from findLocation.py. You can call findLocation.main([...parameters...]) to get the result dictioary.

When you call findLocation.main, the return value is a dictionary with the following keys:
* 'ip\_record\_ratio': a floating point number of the ratio of record ip.
* 'poster': the poster dictionary. It has keys like 'title', 'city', etc.
* 'foreign\_push': all the foreign pushes
* 'taiwan\_push': all the taiwan pushes 
* 'taiwan\_push\_acc' and 'foreign\_push\_acc': the number of pushes for each country/city.
* 'foreign\_push\_id': all the foreigh push id.

It is important to include a chinese font since bydefault pyplot does not support chinese. '思源宋體' is by defualt used by the program, so please download it from [思源宋體](https://www.google.com/get/noto/#serif-hant) and place the 'regular' one in the root directory (should be named as 'NotoSerifCJKtc-Regular.otf'). It is hard coded in genReplyPieChart.

The output plot will be stored in 'gen'.

Or just print the statistic to stdout or whatever place you like.
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
