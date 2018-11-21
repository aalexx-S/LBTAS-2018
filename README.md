# PTT Reply Location Marker

This program use some geolocation magic to find the replyers' location and mark it on a map using [api](https://segis.moi.gov.tw/STAT/Web/Portal/STAT_PortalHome.aspx#) provided by Ministry of the Interior, Taiwan.

## Usage

```
python3 findLocation.py [-h] [-db DATABASE] [-qt QUERYTIMES] [-o OUTPUT | -silent] KEY_FILE INPUT
```

Use -h for more details.

## Key File

Users need to place the api services they want to use and other required information in a file.

Each line contains a service, formatted as follow:

```
SERVICE_NAME [other required information when making requests, like key]
```

I will assume you are using a free trial of all the api, so there will be limitation on each api service. Also, all limitations are hard coded, so if the services change their limits...

Supported services:

* [ipapi](http://ip-api.com/) - 150 requests / min
	* ```
	ipapi
	```

* [geoplugin](https://www.geoplugin.com/) - 2 requests / second
	* ```
	geoplugin
	```

## Input

Input is a web ptt post url. For example: [Gossiping Board Rules](https://www.ptt.cc/bbs/Gossiping/M.1510415718.A.D77.html).

## Dependency

* [pandas](https://pandas.pydata.org/)

* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## IP2Location Database

You can place IP2Location database in the project for faster performance.

All it does is filter the ip that is not in Taiwan.

The database must also include longitude and latitude information.

Please download the CSV one since I don't know what that bin file is.

This site or product includes IP2Location LITE data available from [http://www.ip2location.com](http://www.ip2location.com).
