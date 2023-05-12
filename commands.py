import utils
import points
import profiles
import map_getter

def download(args):
    if len(args) == 0:
        print('USAGE: download [map/all] (start)')
        return
    else:
        mn = args[0]
        if mn == 'all':
            maplist(args)
            start_idx = 0
            if len(args) > 1:
                try:
                    start_idx = int(args[1])
                except ValueError:
                    start_idx = 0
            map_getter.download_all_maps(idx=start_idx)
        else:
            map_getter.download_map(mn)
        
def maplist(args):
    print('Updating map list...')
    utils.fetch_current_maplist()
    print('Map list updated.')
    
def srank(args):
    if len(args) != 1:
        print('USAGE: srank [tempusid/#rank]')
    else:
        p = utils.get_latest_profiles()
        p2 = utils.get_latest_profiles(x=1)
        if p2 is None:
            p2 = p
        if args[0][0] == '#':
            try:
                search_rank = int(args[0][1:])
            except ValueError:
                print('USAGE: srank [tempusid/#rank]')
                return
            for pid in p.keys():
                if p[pid]['rank']['soldier'] == search_rank:
                    name = p[pid]['name']
                    rank = p[pid]['rank']['soldier']
                    oldrank = p2[pid]['rank']['soldier']
                    pts = p[pid]['points']['soldier']
                    oldpts = p2[pid]['points']['soldier']
                    break
            else:
                print('No player found.')
                return
        else:
            uid = args[0]
            if uid not in p.keys():
                print('Player not found.')
                return
            name = p[uid]['name']
            rank = p[uid]['rank']['soldier']
            oldrank = p2[uid]['rank']['soldier']
            pts = p[uid]['points']['soldier']
            oldpts = p2[uid]['points']['soldier']

        rankdelta = rank - oldrank
        rankdelta_string = ' '
        if rankdelta > 0:
            rankdelta_string += '(↓'
        elif rankdelta < 0:
            rankdelta_string += '(↑'
        if rankdelta == 0:
            rankdelta_string = ''
        else:
            rankdelta_string += str(abs(rankdelta)) + ')'
        
        pointsdelta = pts - oldpts
        pointsdelta_string = ''
        if pointsdelta > 0:
            pointsdelta_string += '(+'
        elif pointsdelta < 0:
            pointsdelta_string += '('
        if pointsdelta == 0:
            pointsdelta_string = ''
        else:
            pointsdelta_string += str(int(pointsdelta)) + ')'
        
        print(f'{name}: Rank {rank} soldier{rankdelta_string} | {int(pts)} points {pointsdelta_string}')

def drank(args):
    if len(args) != 1:
        print('USAGE: drank [tempusid/#rank]')
    else:
        p = utils.get_latest_profiles()
        p2 = utils.get_latest_profiles(x=1)
        if p2 is None:
            p2 = p
        if args[0][0] == '#':
            try:
                search_rank = int(args[0][1:])
            except ValueError:
                print('USAGE: drank [tempusid/#rank]')
                return
            for pid in p.keys():
                if p[pid]['rank']['demoman'] == search_rank:
                    name = p[pid]['name']
                    rank = p[pid]['rank']['demoman']
                    oldrank = p2[pid]['rank']['demoman']
                    pts = p[pid]['points']['demoman']
                    oldpts = p2[pid]['points']['demoman']
                    break
            else:
                print('No player found.')
                return
        else:
            uid = args[0]
            if uid not in p.keys():
                print('Player not found.')
                return
            name = p[uid]['name']
            rank = p[uid]['rank']['demoman']
            oldrank = p2[uid]['rank']['demoman']
            pts = p[uid]['points']['demoman']
            oldpts = p2[uid]['points']['demoman']

        rankdelta = rank - oldrank
        rankdelta_string = ' '
        if rankdelta > 0:
            rankdelta_string += '(↓'
        elif rankdelta < 0:
            rankdelta_string += '(↑'
        if rankdelta == 0:
            rankdelta_string = ''
        else:
            rankdelta_string += str(abs(rankdelta)) + ')'
        
        pointsdelta = pts - oldpts
        pointsdelta_string = ''
        if pointsdelta > 0:
            pointsdelta_string += '(+'
        elif pointsdelta < 0:
            pointsdelta_string += '('
        if pointsdelta == 0:
            pointsdelta_string = ''
        else:
            pointsdelta_string += str(int(pointsdelta)) + ')'
        
        print(f'{name}: Rank {rank} demoman{rankdelta_string} | {int(pts)} points {pointsdelta_string}')

def leaderboards(args):
    print('Generating leaderboards...')
    cur_date = utils.get_current_date()
    p = utils.get_latest_profiles()
    p2 = utils.get_latest_profiles(x=1)
    # If no previous profile snapshot, just use the same one (no change)
    if p2 is None:
        p2 = p
    for classname in ('soldier', 'demoman'):
        pids = p.keys()
        pids = sorted(pids, key=lambda x: p[x]['rank'][classname])
        with open(f'{classname}_ranks/{cur_date}.txt', 'w', encoding='utf-8') as f:
            changedate = utils.get_latest_profile_date(x=1)
            f.write(cur_date + ' (Change since ' + changedate + ')' + '\n')
            for pid in pids:
                rank = p[pid]['rank'][classname]
                # Don't include unranked people
                if rank == -1:
                    continue
                name = p[pid]['name']
                points = p[pid]['points'][classname]
                if pid not in p2.keys():
                    oldpoints = 0
                    oldrank = rank
                else:
                    oldpoints = p2[pid]['points'][classname]
                    oldrank = p2[pid]['rank'][classname]
                    if oldrank == -1:
                        oldrank = rank
                
                # Points change from last fetch
                points_delta = int(points - oldpoints)
                points_delta_string = ''
                if points_delta > 0:
                    points_delta_string += '+'
                    
                points_delta_string += str(points_delta)
                
                rank_delta = int(rank - oldrank)
                rank_delta_string = ''
                if rank_delta > 0:
                    rank_delta_string += '↓'
                elif rank_delta < 0:
                    rank_delta_string += '↑'
                    
                rank_delta_string += str(abs(rank_delta))
                
                if rank_delta == 0:
                    rank_delta_string = ''
                
                if points_delta == 0:
                    f.write(f'{rank}. {name}: {int(points)} points {rank_delta_string}\n')
                else:
                    f.write(f'{rank}. {name}: {int(points)} points ({points_delta_string}) {rank_delta_string}\n')

def lookup(args):
    name = ' '.join(args).lower()
    p = utils.get_latest_profiles()
    
    foundnames = []
    for plr in p.keys():
        if name in p[plr]['name'].lower():
            pts = 0
            pts += p[plr]['points']['soldier']
            pts += p[plr]['points']['demoman']
            foundnames.append((p[plr]['name'], plr, pts))
    
    if len(foundnames) == 0:
        print(f'No matches found for {name}')
        return
    
    foundnames = sorted(foundnames, key=lambda x: x[2], reverse=True)
    
    print('Found players: ')
    for nm in foundnames[:20]:
        print(f'(ID {nm[1]}) {nm[0]}')

def stime(args, p=None, p2=None, silent=False):
    if len(args) < 2:
        print('USAGE: stime [tempusid] [map]')
        return
    if p is None:
        p = utils.get_latest_profiles()
    if p2 is None:
        p2 = utils.get_latest_profiles(x=1)
    uid = args[0]
    mn = args[1].lower()
    if uid not in p.keys():
        if not silent:
            print('Player not found.')
        return
    if mn not in p[uid]['runs']['soldier'].keys():
        if not silent:
            print('No time found.')
        return
    if uid not in p2.keys():
        p2 = p
    if mn not in p2[uid]['runs']['soldier'].keys():
        p2 = p
    
    # Get run information
    name = p[uid]['name']
    run = p[uid]['runs']['soldier'][mn]
    rank = run['rank']
    completions = run['completions']
    group = points.in_group(rank, completions)
    group_str = 'NG' if group == -1 else ['TT', 'G1', 'G2', 'G3', 'G4'][group]
    group_str = 'WR' if rank == 1 else group_str
    time_str = utils.tempus_timestring(run['duration'])
    pts = points.points(rank, completions)

    old_run = p2[uid]['runs']['soldier'][mn]
    old_rank = old_run['rank']
    old_completions = old_run['completions']
    old_pts = points.points(old_rank, old_completions)
    
    comp_pts = ' ('
    if pts - old_pts > 0: 
        comp_pts += '+'
    comp_pts += str(int(pts - old_pts)) + ')'
    if int(pts - old_pts) == 0:
        comp_pts = ''

    # Next group up split comparison
    comp_rank, comp_group = utils.get_group_trail(rank, completions)
    md = utils.get_latest_map_data(mn, x=0)
    comp_time = utils.tempus_timestring(run['duration'] - md['results']['soldier'][comp_rank - 1]['duration'])

    print(f'{name} on {mn}: {group_str} @ {time_str} ({comp_group} +{comp_time}) | {rank}/{completions} | Points: {int(pts)}{comp_pts}')

def dtime(args, p=None, p2=None, silent=False):
    if len(args) < 2:
        print('USAGE: dtime [tempusid] [map]')
        return
    if p is None:
        p = utils.get_latest_profiles()
    if p2 is None:
        p2 = utils.get_latest_profiles(x=1)
    uid = args[0]
    mn = args[1].lower()
    if uid not in p.keys():
        if not silent:
            print('Player not found.')
        return
    if mn not in p[uid]['runs']['demoman'].keys():
        if not silent:
            print('No time found.')
        return
    if uid not in p2.keys():
        p2 = p
    if mn not in p2[uid]['runs']['demoman'].keys():
        p2 = p
    
    # Get run information
    name = p[uid]['name']
    run = p[uid]['runs']['demoman'][mn]
    rank = run['rank']
    completions = run['completions']
    group = points.in_group(rank, completions)
    group_str = 'NG' if group == -1 else ['TT', 'G1', 'G2', 'G3', 'G4'][group]
    group_str = 'WR' if rank == 1 else group_str
    time_str = utils.tempus_timestring(run['duration'])
    pts = points.points(rank, completions)

    old_run = p2[uid]['runs']['demoman'][mn]
    old_rank = old_run['rank']
    old_completions = old_run['completions']
    old_pts = points.points(old_rank, old_completions)
    
    comp_pts = ' ('
    if pts - old_pts > 0: 
        comp_pts += '+'
    comp_pts += str(int(pts - old_pts)) + ')'
    if int(pts - old_pts) == 0:
        comp_pts = ''

    # Next group up split comparison
    comp_rank, comp_group = utils.get_group_trail(rank, completions)
    md = utils.get_latest_map_data(mn, x=0)
    comp_time = utils.tempus_timestring(run['duration'] - md['results']['demoman'][comp_rank - 1]['duration'])

    print(f'{name} on {mn}: {group_str} @ {time_str} ({comp_group} +{comp_time}) | {rank}/{completions} | Points: {int(pts)}{comp_pts}')
    
def dtimeall(args):
    uid = args[0]
    ml = utils.get_demoman_maps()
    p = utils.get_latest_profiles()
    p2 = utils.get_latest_profiles(x=1)
    for mn in ml:
        dtime((uid, mn), p=p, p2=p2, silent=True)

def stimeall(args):
    uid = args[0]
    ml = utils.get_soldier_maps()
    p = utils.get_latest_profiles()
    p2 = utils.get_latest_profiles(x=1)
    for mn in ml:
        stime((uid, mn), p=p, p2=p2, silent=True)

def update(args):
    print('Updating tempus data...')
    profiles.build_profiles()
    print('Tempus data updated.')