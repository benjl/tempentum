import requests
import utils
import ssl
from pathlib import Path

# Download a single map
def download_map(mapname, silent=False):
    cur_date = utils.get_current_date()
    if not silent:
        d_maps = utils.get_demoman_maps()
        s_maps = utils.get_soldier_maps()
    else:
        d_maps, s_maps = None, None
        
    try:
        r = requests.get(f'https://tempus2.xyz/api/v0/maps/name/{mapname}/zones/typeindex/map/1/records/list?limit=10000')
    except ssl.SSLError:
        print(f'{mapname} failed to download.')
        return False
    
    if r.status_code != requests.codes.ok or r.text.startswith('{"error"'):
        print(f'{mapname} failed to download.')
        return False
    
    Path(f'internal/times/{mapname}').mkdir(parents=True, exist_ok=True) # Make the folder if it doesn't exist yet
    with open(f'internal/times/{mapname}/{cur_date}.json', 'w', encoding='utf-8') as f:
        f.write(r.text)
    if not silent:
        print(f'{mapname} downloaded.')
        if mapname not in d_maps and mapname not in s_maps:
            print(f'WARNING: {mapname} is not assigned as soldier or demo map.')
    
    return True

def download_all_maps(idx=0):
    maplist = utils.load_maplist()
    mapcount = len(maplist)
    failed = []
    d_maps = utils.get_demoman_maps()
    s_maps = utils.get_soldier_maps()
    for i, mn in enumerate(maplist[idx:], start=idx+1):
        try:
            status = download_map(mn, silent=True)
            if not status:
                failed.append(mn)
                print(f'{i}/{mapcount} Maps Downloaded ({mn} FAILED)')
            else:
                print(f'{i}/{mapcount} Maps Downloaded ({mn})')
        except KeyboardInterrupt:
            print('Map downloads interrupted.')
            break
    
    if len(failed) > 0:
        print(f'WARNING: These maps failed to download: {", ".join(failed)}.')
    
    for mapn in maplist:
        if mapn not in s_maps and mapn not in d_maps:
            print(f'WARNING: {mapn} is not assigned as soldier or demo map.')
    for mapn in s_maps + d_maps:
        if mapn not in maplist and (mapn in s_maps or mapn in d_maps):
            print(f'WARNING: {mapn} is assigned as a demo or soldier map, but is not on tempus.')