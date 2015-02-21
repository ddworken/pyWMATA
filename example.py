import argparse
import pyWMATA
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--start", help="From station")
parser.add_argument("--end", help="To station")
parser.add_argument("--arrivals", help="Arrival times at a given station")
args = parser.parse_args()

apikey = 'kfgpmgvfgacx98de9q3xazww' #Developer key
api = pyWMATA.WMATA(apikey)

if args.start and args.end:
    print api.getPathHumanReadable(args.start,args.end)
    direction = api.getPath(args.start,args.end)[0].split("Start towards ",1)[1][:-1]
    for depTime in api.getTrainDepartures(args.start,direction):
        if depTime >= 0:
            if depTime != 1:
                print "Next departure time from " + args.start + " is in " + str(depTime) + " minutes"
            else:
                print "Next departure time from " + args.start + " is in " + str(depTime) + " minute."
            break
        print depTime
if args.arrivals:
    print "The arrival times at " + args.arrivals + " are: " +  ', '.join(str(x) for x in api.getTrainDepartures(args.arrivals))
if not len(sys.argv) > 1:
    print "Please use at least one argument"
