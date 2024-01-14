import points
import utils
import json


# Builds profiles for all tempus users and stores them in profiles/[date].json
def build_profiles():
    try:
        # Profiles will later be dumped to the .json
        profiles = {}
        cur_date = utils.get_current_date()
        maplist = utils.load_maplist()
        d_maps = utils.get_demoman_maps()
        s_maps = utils.get_soldier_maps()
        total_maps = len(maplist)
        # First we go through each run on each map and add it to the person's profile
        for i, mn in enumerate(maplist):
            data = utils.get_latest_map_data(mn)
            if data is None:
                continue
            for classname in ('demoman', 'soldier'):
                if classname == 'demoman' and mn not in d_maps:
                    continue
                if classname == 'soldier' and mn not in s_maps:
                    continue
                    
                for run in data['results'][classname]:
                    # Set up the initial profile if this is the person's first seen run
                    id = run['user_id']
                    if id not in profiles:
                        profiles[id] = {}
                        profiles[id]['name'] = run['name'].replace('\n',' ')
                        profiles[id]['rank'] = {'soldier': -1, 'demoman': -1}
                        profiles[id]['points'] = {'soldier': 0, 'demoman': 0}
                        profiles[id]['runs'] = {'soldier': {}, 'demoman': {}}

                    profiles[id]['runs'][classname][mn] = {}
                    profiles[id]['runs'][classname][mn]['duration'] = run['duration']
                    profiles[id]['runs'][classname][mn]['rank'] = run['rank']
                    profiles[id]['runs'][classname][mn]['completions'] = data['completion_info'][classname]
                    profiles[id]['points'][classname] += points.points(run['rank'], data['completion_info'][classname])
            if i % (total_maps // 10) == 1:
                print(f'{round(i/total_maps*100)}%...')
        
        # Then we rank every player based on their points
        ids = profiles.keys()
        
        ids = sorted(ids, key=lambda x: profiles[x]['points']['demoman'], reverse=True)
        for rank, plr_id in enumerate(ids, start=1): 
            profiles[plr_id]['rank']['demoman'] = rank
            if profiles[plr_id]['points']['demoman'] == 0:
                profiles[plr_id]['rank']['demoman'] = -1
                
        ids = sorted(ids, key=lambda x: profiles[x]['points']['soldier'], reverse=True)
        for rank, plr_id in enumerate(ids, start=1): 
            profiles[plr_id]['rank']['soldier'] = rank
            if profiles[plr_id]['points']['soldier'] == 0:
                profiles[plr_id]['rank']['soldier'] = -1
        
        with open(f'internal/profiles/{cur_date}.json', 'w') as f:
            json.dump(profiles, f)
    except KeyboardInterrupt:
        print('Update interrupted.')
        return