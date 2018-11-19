# PTT Reply Location Marker

This program use some geolocation magic to find the replyers' location and mark it on a map using [api](https://segis.moi.gov.tw/STAT/Web/Portal/STAT_PortalHome.aspx#) provided by Ministry of the Interior, Taiwan.

## Usage

```
python3 findLocation.py [-h] [-db DATABASE] [-o OUTPUT | -silent] INPUT
```

Use -h for more details.

Set OUTPUT for output file name or silent for no output.

INPUT is the web ptt url.

# IP2Location

You can place IP2Location database in the project for faster performance.

The database must have latitude and longtitude information.

Please download the CSV one since I don't want to deal with sql.

This site or product includes IP2Location LITE data available from [http://www.ip2location.com](http://www.ip2location.com).
