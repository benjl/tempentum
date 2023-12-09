import utils
import points
import profiles
import map_getter

def help(args):
    print("""download all: downloads tempus data from the internet
update: calculate points
rankall: generate leaderboards file""")

def stimes(args):
    if len(args) == 0:
        print('USAGE: stimes [map] ((start-)end)')
        return
    mn = utils.find_map(args[0])
    if mn is None:
        print('Map not found.')
        return
    if mn not in utils.get_soldier_maps():
        print(f'{mn} is not a soldier map.')
        return
    data = utils.get_latest_map_data(mn)
    start = 1
    end = 10
    if len(args) > 1:
        if '-' in args[1]:
            if len(args[1].split('-')) != 2:
                print('USAGE: stimes [map] ((start-)end)/(groupname)')
                return
            start,end = args[1].split('-')
            try:
                start = int(start)
                end = int(end)
            except ValueError:
                print('USAGE: stimes [map] ((start-)end)/(groupname)')
                return
        elif args[1].lower() in ('tt', 'g1', 'g2', 'g3', 'g4', 'ng'):
            start, end = utils.ranks_in_group(len(data['results']['soldier']), args[1].lower())
            if start > len(data['results']['soldier']):
                print(f'No runs in group.')
                return
        else:
            try:
                end = int(args[1])
            except ValueError:
                print('USAGE: stimes [map] ((start-)end)/(groupname)')
                return
    start = 1 if start < 1 else start
    if start > len(data['results']['soldier']):
        start = len(data['results']['soldier'])
    if end > len(data['results']['soldier']):
        end = len(data['results']['soldier'])
    if end - start > 50:
        end = start + 50
    if start > end:
        print('Error: start rank must be smaller than end rank')
        return
    print(f'Runs #{start}-{end} on {mn}:')
    p = utils.get_latest_profiles()
    for x in range(start-1,end):
        c = stime([f"{data['results']['soldier'][x]['player_info']['id']}", mn], p=p, p2=p, silent=True, raw=True)
        clipped_name = c['name'][:12]
        print(f"#{c['rank']:{len(str(end))}}: {clipped_name:13} {c['group_str']} @ {c['time_str']} ({c['comp_group']} +{c['comp_time']}) - {c['points']} points")

def dtimes(args):
    if len(args) == 0:
        print('USAGE: dtimes [map] ((start-)end)/(groupname)')
        return
    mn = utils.find_map(args[0])
    if mn is None:
        print('Map not found.')
        return
    if mn not in utils.get_demoman_maps():
        print(f'{mn} is not a demoman map.')
        return
    data = utils.get_latest_map_data(mn)
    start = 1
    end = 10
    if len(args) > 1:
        if '-' in args[1]:
            if len(args[1].split('-')) != 2:
                print('USAGE: dtimes [map] ((start-)end)/(groupname)')
                return
            start,end = args[1].split('-')
            try:
                start = int(start)
                end = int(end)
            except ValueError:
                print('USAGE: dtimes [map] ((start-)end)/(groupname)')
                return
        elif args[1].lower() in ('tt', 'g1', 'g2', 'g3', 'g4', 'ng'):
            start, end = utils.ranks_in_group(len(data['results']['demoman']), args[1].lower())
            if start > len(data['results']['demoman']):
                print(f'No runs in group.')
                return
        else:
            try:
                end = int(args[1])
            except ValueError:
                print('USAGE: dtimes [map] ((start-)end)/(groupname)')
                return
    start = 1 if start < 1 else start
    if start > len(data['results']['demoman'])+1:
        start = len(data['results']['demoman'])+1
    if end > len(data['results']['demoman']):
        end = len(data['results']['demoman'])
    if end - start > 50:
        end = start + 50
    if start > end:
        print('Error: start rank must be smaller than end rank')
        return
    print(f'Runs #{start}-{end} on {mn}:')
    p = utils.get_latest_profiles()
    for x in range(start-1,end):
        c = dtime([f"{data['results']['demoman'][x]['player_info']['id']}", mn], p=p, p2=p, silent=True, raw=True)
        clipped_name = c['name'][:12]
        print(f"#{c['rank']:{len(str(end))}}: {clipped_name:13} {c['group_str']} @ {c['time_str']} ({c['comp_group']} +{c['comp_time']}) - {c['points']} points")

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
            maplist(args)
            mn = utils.find_map(mn)
            if mn is None:
                print('Map not found.')
                return
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
            if uid not in p2.keys():
                p2 = p
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
            if uid not in p2.keys():
                p2 = p
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
            if changedate is not None:
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

def pts(args):
    if len(args) == 0:
        p = utils.get_latest_profiles()
        p2 = utils.get_latest_profiles(x=1)
        if p2 is None:
            p2 = p
        spoints = 0
        dpoints = 0
        spoints2 = 0
        dpoints2 = 0
        for plr in p.keys():
            spoints += p[plr]['points']['soldier']
            dpoints += p[plr]['points']['demoman']
        for plr in p2.keys():
            spoints2 += p2[plr]['points']['soldier']
            dpoints2 += p2[plr]['points']['demoman']
        sdif = int(spoints - spoints2)
        ddif = int(dpoints - dpoints2)
        print(f'Total soldier points: {int(spoints)} (+{sdif})\nTotal demoman points: {int(dpoints)} (+{ddif})')
    else:
        mn = utils.find_map(args[0])
        if mn is None:
            print('Map not found.')
            return
        if mn in utils.get_soldier_maps():
            spoints = 0
            spoints2 = 0
            data = utils.get_latest_map_data(mn)
            data2 = utils.get_latest_map_data(mn, x=1)
            if data2 is None:
                data2 = data
            completions = len(data['results']['soldier'])
            completions2 = len(data2['results']['soldier'])
            for rank, run in enumerate(data['results']['soldier'], start=1):
                spoints += points.points(rank, completions)
            for rank, run in enumerate(data2['results']['soldier'], start=1):
                spoints2 += points.points(rank, completions2)
            sdif = int(spoints - spoints2)
            sign = ''
            if sdif > 0:
                sign = '+'
            elif sdif < 0:
                sign = '-'
            print(f'Total soldier points on {mn}: {int(spoints)}({sign}{abs(sdif)})')
        if mn in utils.get_demoman_maps():
            dpoints = 0
            dpoints2 = 0
            data = utils.get_latest_map_data(mn)
            data2 = utils.get_latest_map_data(mn, x=1)
            if data2 is None:
                data2 = data
            completions = len(data['results']['demoman'])
            completions2 = len(data2['results']['demoman'])
            for rank, run in enumerate(data['results']['demoman'], start=1):
                dpoints += points.points(rank, completions)
            for rank, run in enumerate(data2['results']['demoman'], start=1):
                dpoints2 += points.points(rank, completions2)
            ddif = int(dpoints - dpoints2)
            sign = ''
            if ddif > 0:
                sign = '+'
            elif ddif < 0:
                sign = '-'
            print(f'Total demoman points on {mn}: {int(dpoints)}({sign}{abs(ddif)})')


def sgroups(args):
    if len(args) != 1:
        print('USAGE: sgroups [tempusid]')
        return
    p = utils.get_latest_profiles()
    uid = args[0]
    if uid not in p.keys():
        print('Player not found.')
        return
    groups = [0, 0, 0, 0, 0, 0, 0] # wr, tt, g1, g2, g3, g4, ng
    groupspts = [0, 0, 0, 0, 0, 0, 0]
    groupspct = [0, 0, 0, 0, 0, 0, 0]
    name = p[uid]['name']
    for run in p[uid]['runs']['soldier']:
        r = p[uid]['runs']['soldier'][run]
        if r['rank'] == 1:
            groups[0] += 1
            groupspts[0] += points.points(r['rank'], r['completions'])
        else:
            group = points.in_group(r['rank'], r['completions'])
            if group == -1:
                groups[6] += 1
                groupspts[6] += points.points(r['rank'], r['completions'])
            else:
                groups[group+1] += 1
                groupspts[group+1] += points.points(r['rank'], r['completions'])
    total = sum(groups)
    for i,x in enumerate(groups):
        groupspct[i] = round((x/total)*100, 2)
    print(f"""{name} total soldier runs: {total} ({int(sum(groupspts))} pts)
    WR: {groups[0]}({groupspct[0]}%)({int(groupspts[0])} pts)
    TT: {groups[1]}({groupspct[1]}%)({int(groupspts[1])} pts)
    G1: {groups[2]}({groupspct[2]}%)({int(groupspts[2])} pts)
    G2: {groups[3]}({groupspct[3]}%)({int(groupspts[3])} pts)
    G3: {groups[4]}({groupspct[4]}%)({int(groupspts[4])} pts)
    G4: {groups[5]}({groupspct[5]}%)({int(groupspts[5])} pts)
    NG: {groups[6]}({groupspct[6]}%)({int(groupspts[6])} pts)""")
    
def dgroups(args):
    if len(args) != 1:
        print('USAGE: dgroups [tempusid]')
        return
    p = utils.get_latest_profiles()
    uid = args[0]
    if uid not in p.keys():
        print('Player not found.')
        return
    groups = [0, 0, 0, 0, 0, 0, 0] # wr, tt, g1, g2, g3, g4, ng
    groupspts = [0, 0, 0, 0, 0, 0, 0]
    groupspct = [0, 0, 0, 0, 0, 0, 0]
    name = p[uid]['name']
    for run in p[uid]['runs']['demoman']:
        r = p[uid]['runs']['demoman'][run]
        if r['rank'] == 1:
            groups[0] += 1
            groupspts[0] += points.points(r['rank'], r['completions'])
        else:
            group = points.in_group(r['rank'], r['completions'])
            if group == -1:
                groups[6] += 1
                groupspts[6] += points.points(r['rank'], r['completions'])
            else:
                groups[group+1] += 1
                groupspts[group+1] += points.points(r['rank'], r['completions'])
    total = sum(groups)
    for i,x in enumerate(groups):
        groupspct[i] = round((x/total)*100, 2)
    print(f"""{name} total demoman runs: {total} ({int(sum(groupspts))} pts)
    WR: {groups[0]}({groupspct[0]}%)({int(groupspts[0])} pts)
    TT: {groups[1]}({groupspct[1]}%)({int(groupspts[1])} pts)
    G1: {groups[2]}({groupspct[2]}%)({int(groupspts[2])} pts)
    G2: {groups[3]}({groupspct[3]}%)({int(groupspts[3])} pts)
    G3: {groups[4]}({groupspct[4]}%)({int(groupspts[4])} pts)
    G4: {groups[5]}({groupspct[5]}%)({int(groupspts[5])} pts)
    NG: {groups[6]}({groupspct[6]}%)({int(groupspts[6])} pts)""")

def stime(args, p=None, p2=None, silent=None, raw=None):
    raw = False if raw is None else raw
    silent = False if silent is None else silent
    if len(args) < 2:
        print('USAGE: stime [tempusid] [map]')
        return
    if p is None:
        p = utils.get_latest_profiles()
    if p2 is None:
        p2 = utils.get_latest_profiles(x=1)
    if p2 is None:
        p2 = p
    uid = args[0]
    mn = utils.find_map(args[1])
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
    new_completion = False
    if mn not in p2[uid]['runs']['soldier'].keys():
        p2 = p
        new_completion = True
    
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
    if new_completion:
        old_pts = 0
    comp_pts = ' ('
    if pts - old_pts > 0: 
        comp_pts += '+'
    comp_pts += str(int(pts - old_pts)) + ')'
    if int(pts - old_pts) == 0:
        comp_pts = ''

    # Next group up split comparison
    comp_rank, comp_group = utils.get_group_trail(rank, completions)
    md = utils.get_latest_map_data(mn, x=0)
    if md is not None:
        comp_time = utils.tempus_timestring(run['duration'] - md['results']['soldier'][comp_rank - 1]['duration'])
    else:
        comp_time = 0
    if raw:
        return {
            'name': name,
            'mapname': mn,
            'group_str': group_str,
            'time_str': time_str,
            'comp_group': comp_group,
            'comp_time': comp_time,
            'rank': rank,
            'completions': completions,
            'points': int(pts),
            'comp_pts': comp_pts 
        }
    print(f'{name} on {mn}: {group_str} @ {time_str} ({comp_group} +{comp_time}) | {rank}/{completions} | Points: {int(pts)}{comp_pts}')

def dtime(args, p=None, p2=None, silent=None, raw=None):
    raw = False if raw is None else raw
    silent = False if silent is None else silent
    if len(args) < 2:
        print('USAGE: dtime [tempusid] [map]')
        return
    if p is None:
        p = utils.get_latest_profiles()
    if p2 is None:
        p2 = utils.get_latest_profiles(x=1)
    if p2 is None:
        p2 = p
    uid = args[0]
    mn = utils.find_map(args[1])
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
    new_completion = False
    if mn not in p2[uid]['runs']['demoman'].keys():
        p2 = p
        new_completion = True
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
    if new_completion:
        old_pts = 0
    comp_pts = ' ('
    if pts - old_pts > 0: 
        comp_pts += '+'
    comp_pts += str(int(pts - old_pts)) + ')'
    if int(pts - old_pts) == 0:
        comp_pts = ''

    # Next group up split comparison
    comp_rank, comp_group = utils.get_group_trail(rank, completions)
    md = utils.get_latest_map_data(mn, x=0)
    if md is not None:
        comp_time = utils.tempus_timestring(run['duration'] - md['results']['demoman'][comp_rank - 1]['duration'])
    else:
        comp_time = 0
    if raw:
        return {
            'name': name,
            'mapname': mn,
            'group_str': group_str,
            'time_str': time_str,
            'comp_group': comp_group,
            'comp_time': comp_time,
            'rank': rank,
            'completions': completions,
            'points': int(pts),
            'comp_pts': comp_pts 
        }

    print(f'{name} on {mn}: {group_str} @ {time_str} ({comp_group} +{comp_time}) | {rank}/{completions} | Points: {int(pts)}{comp_pts}')
    
def dtimeall(args):
    uid = args[0]
    groupname = None
    if len(args) > 1:
        groupname = args[1].lower()
        name_to_number = {'tt': 0, 'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'ng': -1}
        if groupname not in name_to_number:
            print(f'Unknown group "{groupname}"')
            return
        groupnumber = name_to_number[groupname]
    p = utils.get_latest_profiles()
    if uid not in p:
        print('User id not found.')
        return
    p2 = utils.get_latest_profiles(x=1)
    print(f'Showing demoman times for {p[uid]["name"]}:')
    for run in p[uid]['runs']['demoman']:
        r = p[uid]['runs']['demoman'][run]
        if groupname:
            if points.in_group(r['rank'], r['completions']) == groupnumber:
                d = dtime((uid, run), p=p, p2=p2, silent=True, raw=True)
                group_time_comp = f"{d['group_str']} @ {d['time_str']} ({d['comp_group']} +{d['comp_time']})"
                rank_str = f"{d['rank']}/{d['completions']}"
                print(f"{d['mapname'][:20]:20} | {group_time_comp:32} | {rank_str:9} | Points: {d['points']}{d['comp_pts']}")

        else:
            d = dtime((uid, run), p=p, p2=p2, silent=True, raw=True)
            group_time_comp = f"{d['group_str']} @ {d['time_str']} ({d['comp_group']} +{d['comp_time']})"
            rank_str = f"{d['rank']}/{d['completions']}"
            print(f"{d['mapname'][:20]:20} | {group_time_comp:32} | {rank_str:9} | Points: {d['points']}{d['comp_pts']}")


def stimeall(args):
    uid = args[0]
    groupname = None
    if len(args) > 1:
        groupname = args[1].lower()
        name_to_number = {'tt': 0, 'g1': 1, 'g2': 2, 'g3': 3, 'g4': 4, 'ng': -1}
        if groupname not in name_to_number:
            print(f'Unknown group "{groupname}"')
            return
        groupnumber = name_to_number[groupname]
    p = utils.get_latest_profiles()
    if uid not in p:
        print('User id not found.')
        return
    p2 = utils.get_latest_profiles(x=1)
    print(f'Showing soldier times for {p[uid]["name"]}:')
    for run in p[uid]['runs']['soldier']:
        r = p[uid]['runs']['soldier'][run]
        if groupname:
            if points.in_group(r['rank'], r['completions']) == groupnumber:
                d = stime((uid, run), p=p, p2=p2, silent=True, raw=True)
                group_time_comp = f"{d['group_str']} @ {d['time_str']} ({d['comp_group']} +{d['comp_time']})"
                rank_str = f"{d['rank']}/{d['completions']}"
                print(f"{d['mapname'][:20]:20} | {group_time_comp:32} | {rank_str:9} | Points: {d['points']}{d['comp_pts']}")
        else:
            d = stime((uid, run), p=p, p2=p2, silent=True, raw=True)
            group_time_comp = f"{d['group_str']} @ {d['time_str']} ({d['comp_group']} +{d['comp_time']})"
            rank_str = f"{d['rank']}/{d['completions']}"
            print(f"{d['mapname'][:20]:20} | {group_time_comp:32} | {rank_str:9} | Points: {d['points']}{d['comp_pts']}")


def id(args):
    if len(args) < 1:
        print('USAGE: id [playername]')
        return
    name = ' '.join(args)
    p = utils.get_latest_profiles()
    for id in p:
        if p[id]['name'].lower().startswith(name.lower()):
            print(f'{p[id]["name"]}: {id}')
def update(args):
    print('Updating tempus data...')
    profiles.build_profiles()
    print('Tempus data updated.')