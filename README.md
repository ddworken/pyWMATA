# pyWMATA
A python library for accessing the WMATA API for Washington DC Metro. 
##Usage
```python
  apikey = '' ###API keys available here https://developer.wmata.com/

  api = WMATA(apikey)
```
=====
To get departure times for a given stationcode
```python
  stationcode = 'F01' #Gallery place metro

  times = api.getTrainDepartures(stationcode)
```
Returns a list of times until train departures from the given station. 
=====
To get departure times for a given stationcode in a certain direction
```python
  stationcode = 'F01' #Gallery place metro
  
  times = api.getTrainDepartures(stationcode, 'Huntington', 'Franconia-Springfield')
  ```
Returns a list of times until train departures from the given station in the given direction. 
=====
To get travel time needed to travel from one station to another
```python
  startStationCode = 'F01' #Gallery place metro
  endStationCode = 'A04' #Woodley Park metro
  
  totalTravelTime = getTravelTime(self, startStationCode, endStationCode)
```
Returns an integer that is the total time needed to go from one station to the next.
=====
To get a path from one station to another 
Note: This requires that the two stations be on the same line, this will not work with stations on different lines.
```python
  startStationCode = 'F01' #Gallery place metro
  
  endStationCode = 'A04' #Woodley Park metro
  
  stopsAlongPath = getPath(startStationCode, endStationCode)
````
Returns a list of station names along the path
