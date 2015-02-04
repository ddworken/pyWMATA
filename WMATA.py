import urllib2
from xml.dom.minidom import parseString

class WMATA(object):
    def __init__(self, apikey):
        self.apikey = apikey
    def getTrainDepartures(self, stationcode, *direction):
        dom = self.getDom('http://api.wmata.com/StationPrediction.svc/GetPrediction/' + stationcode + '&')
        arrivalTimes = []
        if not direction:
            for index,item in enumerate(dom.getElementsByTagName('Min')):
                arrivalTimes.append(self.processTimeToInt(item.toxml()))
            return arrivalTimes
        for index,item in enumerate(dom.getElementsByTagName('Min')):
            for directionStr in direction:
                if directionStr.lower() in dom.getElementsByTagName('DestinationName')[index].toxml().lower():
                    arrivalTimes.append(self.processTimeToInt(item.toxml()))
        return arrivalTimes

    def getConnectionTimes(self, startArrivalTimes, endArrivalTimes, startStationCode, endStationCode):
        output = [["" for x in range(10)] for x in range(10)]
        for indexStart,itemStart in enumerate(startArrivalTimes):
            for indexEnd,itemEnd in enumerate(endArrivalTimes):
                output[indexStart][indexEnd] = itemEnd - (itemStart + self.getTravelTime(startStationCode, endStationCode))
        return output

    def processTimeToInt(self, xml):
        return int(xml.lower().replace('<min>','').replace('</min>','').replace('brd','0').replace('arr', '0'))

    def getTravelTime(self, startStationCode, endStationCode):
        dom = self.getDom('https://api.wmata.com/Rail.svc/SrcStationToDstStationInfo?FromStationCode=' + startStationCode + '&ToStationCode=' + endStationCode + '&')
        return int(dom.getElementsByTagName('RailTime')[0].toxml().lower().replace('<railtime>','').replace('</railtime>',''))

    def getLines(self, stationCode):
        lines = []
        dom = self.getDom('https://api.wmata.com/Rail.svc/StationInfo?StationCode=' + stationCode + '&')
        lines.append(str(dom.getElementsByTagName('LineCode1')[0].toxml().replace('<LineCode1>','').replace('</LineCode1>','').replace('<LineCode1 i:nil="true"/>','')))
        lines.append(str(dom.getElementsByTagName('LineCode2')[0].toxml().replace('<LineCode2>','').replace('</LineCode2>','').replace('<LineCode2 i:nil="true"/>','')))
        lines.append(str(dom.getElementsByTagName('LineCode3')[0].toxml().replace('<LineCode3>','').replace('</LineCode3>','').replace('<LineCode3 i:nil="true"/>','')))
        lines.append(str(dom.getElementsByTagName('LineCode4')[0].toxml().replace('<LineCode4>','').replace('</LineCode4>','').replace('<LineCode4 i:nil="true"/>','')))
        lines = filter(None, lines)
        return lines

    def getPath(self, startStationCode, endStationCode):
        startLines = self.getLines(startStationCode)
        endLines = self.getLines(endStationCode)
        for startLine in startLines:
            for endLine in endLines:
                if startLine == endLine:
                    sameLine = startLine
                    print self.getTravelTime(startStationCode, endStationCode)
                    return self.getPathSameLine(startStationCode, endStationCode)

    def getPathSameLine(self, startStationCode, endStationCode):
        dom = self.getDom('https://api.wmata.com/Rail.svc/Path?FromStationCode=' + startStationCode + '&ToStationCode=' + endStationCode + '&')
        stations = []
        for item in dom.getElementsByTagName('StationName'):
            item = item.toxml()
            stations.append(item.replace('<StationName>','').replace('</StationName>','').encode("ascii"))
        return stations

    def getIncidents(self):
        dom = self.getDom('https://api.wmata.com/Incidents.svc/Incidents?')
        incidents = []
        for incident in dom.getElementsByTagName('Description'):
            incidents.append(incident.toxml())
        return incidents

    def getIncidentsOnLine(self, line):
        dom = self.getDom('https://api.wmata.com/Incidents.svc/Incidents?')
        incidents = []
        for incidentIndex,incident in enumerate(dom.getElementsByTagName('Description')):
            if line in dom.getElementByTagName('LinesAffected')[incidentIndex].toxml():
                incidents.append(incident.toxml())
        return incidents

    def getStationcode(self, stationname):
        dom = self.getDom('https://api.wmata.com/Rail.svc/Stations?')
        for nameIndex,name in enumerate(dom.getElementsByTagName('Name')):
            if stationname.lower() in name.toxml().lower():
                return dom.getElementsByTagName('Code')[nameIndex].toxml().replace('<Code>','').replace('</Code>','')


    def getDom(self, url):
        try:
            xml = urllib2.urlopen(url + 'api_key=' + self.apikey + '&subscription-key=' + self.apikey)
            return parseString(xml.read())
        except:
            print "Network communication error"
