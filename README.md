# cycling-weather-bot
Pull a local UK forecast from Met Office & pollution forecast from UK-AIR and tweet rain / wind / UV warnings for cycling.

Pre-requisites:
  - Python 3 and packages listed in files (Tweepy, beautifulsoup4, and their dependencies including lxml)
  - Met Office developer key: http://www.metoffice.gov.uk/datapoint/getting-started
  - Twitter account for bot (if using Tweet functionality)
  
Customising your location:
  - Look up the Met Office forecast site ID using http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/sitelist?key=MET_API_KEY, substituting your Met Office API key, and assign it to LOCATION_ID in main.py
  - Search for your location on https://uk-air.defra.gov.uk/ and choose the nearest monitoring site(s). Enter their names in ALL CAPS (i.e. as they appear in the UK_AIR RSS feed - https://uk-air.defra.gov.uk/assets/rss/forecast.xml) in pollution.py.
