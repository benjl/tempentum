import requests
import points
import json
import time
import os

def get_current_date():
    return time.strftime('%Y-%m-%d')

# Fetches maplist and caches it in internal/maplist.json
def fetch_current_maplist():
    r = requests.get('https://tempus2.xyz/api/v0/maps/detailedList')
    if r.status_code != requests.codes.ok:
        print('WARNING: Maplist failed to download.')
        return False
    ml = r.json()
    with open('internal/maplist.json', 'w') as f:
        json.dump(ml, f)

# Loads maplist from internal/maplist.json
def load_maplist():
    with open('internal/maplist.json', 'r') as f:
        ml = json.load(f)
    
    maplist = []
    for m in ml:
        maplist.append(m['name'])
    
    return maplist

# Formats a duration, in seconts to the tempus duration format hh:mm:ss.00
def tempus_timestring(duration):
    if duration >= 3600:
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        seconds = round(seconds, 2)
        run_time = '{}:{:02}:{:05.2f}'.format(int(hours), int(minutes), seconds)
    else:
        minutes, seconds = divmod(duration, 60)
        seconds = round(seconds, 2)
        run_time = '{:02}:{:05.2f}'.format(int(minutes), seconds)
    return run_time

# Return the x+1st most recently downloaded map data
def get_latest_map_data(mapname, x=0):
    try:
        filelist = os.listdir('internal/times/' + mapname)
    except FileNotFoundError:
        print(f'WARNING: {mapname} data not found.')
        return
    if len(filelist) == 0:
        print(f'WARNING: No data for {mapname}.')
        return None
    times = []
    for f in filelist:
        times.append(time.strptime(f.strip('.json'), '%Y-%m-%d'))
    times = sorted(times, reverse=True)
    filename = time.strftime('%Y-%m-%d', times[x]) + '.json'
    with open(f'internal/times/{mapname}/{filename}', 'r', encoding='utf-8') as f:
        mapdata = json.load(f)
    return mapdata

def get_latest_profiles(x=0):
    filelist = os.listdir('internal/profiles/')
    if len(filelist) == 0:
        print(f'WARNING: No profile data.')
        return None
    if x > len(filelist) - 1:
        return None
    times = []
    for f in filelist:
        times.append(time.strptime(f.strip('.json'), '%Y-%m-%d'))
    times = sorted(times, reverse=True)
    filename = time.strftime('%Y-%m-%d', times[x]) + '.json'
    with open(f'internal/profiles/{filename}', 'r') as f:
        profiledata = json.load(f)
    return profiledata

def get_latest_profile_date(x=0):
    filelist = os.listdir('internal/profiles/')
    if len(filelist) == 0:
        print(f'WARNING: No profile data.')
        return None
    if x > len(filelist) - 1:
        return None
    times = []
    for f in filelist:
        times.append(time.strptime(f.strip('.json'), '%Y-%m-%d'))
    times = sorted(times, reverse=True)
    date = time.strftime('%Y-%m-%d', times[x])
    return date

def get_soldier_maps():
    mapnames = []
    with open('internal/soldier_maps.txt', 'r') as f:
        for x in f.readlines():
            d = x.strip(' \t\n')
            mapnames.append(d)
    mapnames = sorted(mapnames)
    return mapnames
    
    
def get_demoman_maps():
    mapnames = []
    with open('internal/demoman_maps.txt', 'r') as f:
        for x in f.readlines():
            d = x.strip(' \t\n')
            mapnames.append(d)
    mapnames = sorted(mapnames)
    return mapnames

# Return the last place in the group above the given time and the group name
def get_group_trail(rank, completions):
    groups = points.groupsizes(completions)

    grouptrail = 0
    if points.in_group(rank, completions) == 0:
        compstr = 'WR'
        grouptrail = 1
    elif points.in_group(rank, completions) == 1:
        compstr = 'TT'
        grouptrail = 10
    elif points.in_group(rank, completions) == 2:
        compstr = 'G1'
        grouptrail = 10+groups[0]
    elif points.in_group(rank, completions) == 3:
        compstr = 'G2'
        grouptrail = 10+groups[0]+groups[1]
    elif points.in_group(rank, completions) == 4:
        compstr = 'G3'
        grouptrail = 10+groups[0]+groups[1]+groups[2]
    else:
        compstr = 'G4'
        grouptrail = 10+groups[0]+groups[1]+groups[2]+groups[3]
    
    return (grouptrail, compstr)