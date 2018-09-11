from __future__ import print_function
import ephem
import cv2
import sys
import math
import imutils
import datetime

if len(sys.argv) != 9:
    print('Proper usage: python transitsearch.py lat(N+) long(E+) elevation(m) yyyy-mm-dd hh:mm:ss tle.txt sun/moon duration_of_search(days)')
    exit()

observer = ephem.Observer()
observer.lat = sys.argv[1]
observer.lon = sys.argv[2]
observer.elevation = float(sys.argv[3])
observer.date = str(sys.argv[4]+" "+sys.argv[5])
d = ephem.Date(str(sys.argv[4]+" "+sys.argv[5]))
with open(str(sys.argv[6])) as f:
    lines = [line.rstrip('\n') for line in f]
satcount = int(len(lines)/3)
if str(sys.argv[7]).lower() == str('sun'):
    for t in range(0,(86400*int(sys.argv[8])),1):
        observer.date = (d.datetime() + datetime.timedelta(seconds=t))
        sun = ephem.Sun(observer)
        if sun.alt > 0:
            print(observer.date, end='\r')
            for s in range(0,satcount,3):
                sat = ephem.readtle(lines[s],lines[(s+1)],lines[(s+2)])
                try:
                    sat.compute(observer)
                    separation = ephem.separation((sun.ra, sun.dec),(sat.ra, sat.dec))
                    if separation < sun.radius:
                        print('Transit at ', observer.date, 'Satellite name:', lines[s], 'Sun alt:', sun.alt, "Sun az:", sun.az)
                except:
                    pass
elif str(sys.argv[7]).lower() == str('moon'):
    for t in range(0,(86400*int(sys.argv[8])),1):
        observer.date = (d.datetime() + datetime.timedelta(seconds=t))
        moon = ephem.Moon(observer)
        if moon.alt > 0:
            print(observer.date, end='\r')
            for s in range(0,satcount,3):
                sat = ephem.readtle(lines[s],lines[(s+1)],lines[(s+2)])
                try:
                    sat.compute(observer)
                    separation = ephem.separation((moon.ra, moon.dec),(sat.ra, sat.dec))
                    if separation < moon.radius:
                        print('Transit at ', observer.date, 'Satellite name:', lines[s], 'Moon alt:', moon.alt, "Moon az:", moon.az)
                except:
                    pass
else:
    print('Please specify either moon or sun for transit predictions.  Exiting.')
    exit()


    
