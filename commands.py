import utils
import points
import profiles
import map_getter

def stimes(args):
    """stimes [map] ((start-)end)/groupname
    Prints the specified range of times on the map. Example: stimes beef 40-50 | Prints ranks 40 to 50 on jump_beef.
    Can also print the top of the specified group. Example: stimes beef g3 | Prints the top 50 times in group 3."""
    if len(args) == 0:
        print('No arguments specified.')
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
                print('Invalid syntax.')
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
    md = utils.get_latest_map_data(mn)
    for x in range(start-1,end):
        c = stime([f"{data['results']['soldier'][x]['player_info']['id']}", mn], p=p, p2=p, silent=True, raw=True, md=md)
        clipped_name = c['name'][:12]
        print(f"#{c['rank']:{len(str(end))}}: {clipped_name:13} {c['group_str']} @ {c['time_str']} ({c['comp_group']} +{c['comp_time']}) - {c['points']} points")

def dtimes(args):
    """dtimes [map] ((start-)end)/groupname
    Prints the specified range of times on the map. Example: dtimes aando 40-50 | Prints ranks 40 to 50 on jump_aando.
    Can also print the top of the specified group. Example: dtimes aando g3 | Prints the top 50 times in Group 3."""
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
    md = utils.get_latest_map_data(mn)
    for x in range(start-1,end):
        c = dtime([f"{data['results']['demoman'][x]['player_info']['id']}", mn], p=p, p2=p, silent=True, raw=True, md=md)
        clipped_name = c['name'][:12]
        print(f"#{c['rank']:{len(str(end))}}: {clipped_name:13} {c['group_str']} @ {c['time_str']} ({c['comp_group']} +{c['comp_time']}) - {c['points']} points")

def download(args):
    """download [map/all] (start)
    download all | Downloads map data for every map on tempus.
    download all 266 | Downloads map data for every map on tempus, excluding the first 265 maps in the maplist.
    download map | Downloads map data for a specific map.
    Use update to calculate points and ranks based on downloaded map data."""
    if len(args) == 0:
        print('No arguments specified.')
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
    """maplist | Updates the maplist from tempus."""
    print('Updating map list...')
    utils.fetch_current_maplist()
    print('Map list updated.')
    
def srank(args):
    """srank [tempusid/#rank]
    srank 1137 | Shows the soldier rank of the player with the tempus id 1137. Use the id command to find the id for a given player name.
    srank #30 | Shows who the rank 30 soldier is."""
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
        rankdelta_string = ' ' + utils.rank_delta_string(rankdelta, brackets=True)

        pointsdelta = pts - oldpts
        pointsdelta_string = utils.points_delta_string(pointsdelta, brackets=True)

        print(f'{name}: Rank {rank} soldier{rankdelta_string} | {int(pts)} points {pointsdelta_string}')

def drank(args):
    """drank [tempusid/#rank]
    drank 1137 | Shows the demoman rank of the player with the tempus id 1137. Use the id command to find the id for a given player name.
    drank #30 | Shows who the rank 30 demoman is."""
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
        rankdelta_string = ' ' + utils.rank_delta_string(rankdelta, brackets=True)

        pointsdelta = pts - oldpts
        pointsdelta_string = utils.points_delta_string(pointsdelta, brackets=True)

        print(f'{name}: Rank {rank} demoman{rankdelta_string} | {int(pts)} points {pointsdelta_string}')

def dgainers(args):
    """dgainers (n/losers) | Shows the top n players by demoman points gained. Defaults to 10 if n is omitted.
    dgainers losers (n) | Show the top 10 losers instead."""
    losers = False
    if len(args) == 0:
        n = 10
    else:
        if args[0].lower() == 'losers':
            losers = True
            if len(args) > 1:
                try:
                    n = min(50, int(args[1]))
                except ValueError:
                    print('Invalid argument.')
                    return
                if n < 1:
                    print('n must be more than 0.')
                    return
            else:
                n = 10
        else:
            try:
                n = min(50, int(args[0]))
            except ValueError:
                print('Invalid argument.')
                return
            if n < 1:
                print('n must be more than 0.')
                return
    p = utils.get_latest_profiles()
    p2 = utils.get_latest_profiles(x=1)
    if p2 is None:
        print('No gains found.')
        return
    changedate = utils.get_latest_profile_date(x=1)
    gainers = {}

    for pid in p.keys():
        rank = p[pid]['rank']['demoman']
        if rank == -1:
            continue
        points = p[pid]['points']['demoman']
        if pid not in p2.keys():
            oldpoints = 0
            oldrank = rank
        else:
            oldpoints = p2[pid]['points']['demoman']
            oldrank = p2[pid]['rank']['demoman']
            if oldrank == -1:
                oldrank = rank
        gainers[pid] = {'pts_delta': int(points - oldpoints), 'rank_delta': rank - oldrank}
    pids = gainers.keys()
    pids = sorted(pids, key=lambda x: gainers[x]['pts_delta'])
    what = 'losers'
    if not losers:
        pids = pids[::-1]
        what = 'gainers'
    print(f'Top demoman {what} since {utils.get_latest_profile_date(x=1)}:')
    for i, pid in enumerate(pids[:n], start=1):
        name = p[pid]['name']
        rank = p[pid]['rank']['demoman']
        points = p[pid]['points']['demoman']

        points_delta = gainers[pid]['pts_delta']
        points_delta_string = utils.points_delta_string(points_delta, brackets=True)

        rank_delta = gainers[pid]['rank_delta']
        rank_delta_string = ' ' + utils.rank_delta_string(rank_delta, brackets=True)

        rank_str = f'Rank {rank}{rank_delta_string}'
        gainer_rank = f'{i}.'

        print(f'{gainer_rank:{len(str(n))+2}}{name[:16]:16}| {rank_str:16} | {int(points):6} points {points_delta_string}')

def sgainers(args):
    """sgainers (n) | Shows the top n players by soldier points gained. Defaults to 10 if n is omitted.
    sgainers losers (n) | Show the top n losers instead."""
    losers = False
    if len(args) == 0:
        n = 10
    else:
        if args[0].lower() == 'losers':
            losers = True
            if len(args) > 1:
                try:
                    n = min(50, int(args[1]))
                except ValueError:
                    print('Invalid argument.')
                    return
                if n < 1:
                    print('n must be more than 0.')
                    return
            else:
                n = 10
        else:
            try:
                n = min(50, int(args[0]))
            except ValueError:
                print('Invalid argument.')
                return
            if n < 1:
                print('n must be more than 0.')
                return
    p = utils.get_latest_profiles()
    p2 = utils.get_latest_profiles(x=1)
    if p2 is None:
        print('No gains found.')
        return
    changedate = utils.get_latest_profile_date(x=1)
    gainers = {}

    for pid in p.keys():
        rank = p[pid]['rank']['soldier']
        if rank == -1:
            continue
        points = p[pid]['points']['soldier']
        if pid not in p2.keys():
            oldpoints = 0
            oldrank = rank
        else:
            oldpoints = p2[pid]['points']['soldier']
            oldrank = p2[pid]['rank']['soldier']
            if oldrank == -1:
                oldrank = rank
        gainers[pid] = {'pts_delta': int(points - oldpoints), 'rank_delta': rank - oldrank}
    pids = gainers.keys()
    pids = sorted(pids, key=lambda x: gainers[x]['pts_delta'])
    what = 'losers'
    if not losers:
        pids = pids[::-1]
        what = 'gainers'
    print(f'Top soldier {what} since {utils.get_latest_profile_date(x=1)}:')
    for i, pid in enumerate(pids[:n], start=1):
        name = p[pid]['name']
        rank = p[pid]['rank']['soldier']
        points = p[pid]['points']['soldier']

        points_delta = gainers[pid]['pts_delta']
        points_delta_string = utils.points_delta_string(points_delta, brackets=True)

        rank_delta = gainers[pid]['rank_delta']
        rank_delta_string = utils.rank_delta_string(rank_delta, brackets=True)

        rank_str = f'Rank {rank}{rank_delta_string}'
        gainer_rank = f'{i}.'

        print(f'{gainer_rank:{len(str(n))+2}}{name[:16]:16}| {rank_str:16} | {int(points):6} points {points_delta_string}')

def leaderboards(args):
    """leaderboards | Outputs the complete leaderboards for soldier and demoman to txt files in the soldier_ranks and demoman_ranks folders."""
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
                points_delta_string = utils.points_delta_string(points_delta, brackets=True) + ' '
                if points_delta == 0:
                    points_delta_string = ''

                rank_delta = int(rank - oldrank)
                rank_delta_string = utils.rank_delta_string(rank_delta, brackets=False)
                
                f.write(f'{rank}. {name}: {int(points)} points {points_delta_string}{rank_delta_string}\n')

def pts(args):
    """pts (mapname) | Displays the total number of points that have been earned on a given map, or all maps combined if mapname is omitted."""
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
            diff_string = utils.points_delta_string(sdif, brackets=True)
            print(f'Total soldier points on {mn}: {int(spoints)} {diff_string}')
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
            diff_string = utils.points_delta_string(ddif, brackets=True)
            print(f'Total demoman points on {mn}: {int(dpoints)} {diff_string}')


def sgroups(args):
    """sgroups [tempusid] | Shows how many soldier times in each group a player has."""
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
    """dgroups [tempusid] | Shows how many demoman times in each group a player has."""
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

def stime(args, p=None, p2=None, silent=None, raw=None, md=None):
    """stime [tempusid] [map] | Displays a given player's soldier time on a map."""
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
    comp_pts = utils.points_delta_string(pts - old_pts, brackets=True)

    # Next group up split comparison
    comp_rank, comp_group = utils.get_group_trail(rank, completions)
    if md is None:
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
    print(f'{name} on {mn}: {group_str} @ {time_str} ({comp_group} +{comp_time}) | {rank}/{completions} | Points: {int(pts)} {comp_pts}')

def dtime(args, p=None, p2=None, silent=None, raw=None, md=None):
    """dtime [tempusid] [map] | Displays a given player's demoman time on a map."""
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
    comp_pts = utils.points_delta_string(pts - old_pts, brackets=True)

    # Next group up split comparison
    comp_rank, comp_group = utils.get_group_trail(rank, completions)
    if md is None:
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

    print(f'{name} on {mn}: {group_str} @ {time_str} ({comp_group} +{comp_time}) | {rank}/{completions} | Points: {int(pts)} {comp_pts}')

def dtimeall(args):
    """dtimeall [tempusid] (group) | Displays all of a player's demoman times in the specified group, or all times if group is omitted."""
    if len(args) == 0:
        print('Invalid number of arguments.')
        return
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
                print(f"{d['mapname'][:20]:20} | {group_time_comp:32} | {rank_str:9} | Points: {d['points']} {d['comp_pts']}")

        else:
            d = dtime((uid, run), p=p, p2=p2, silent=True, raw=True)
            group_time_comp = f"{d['group_str']} @ {d['time_str']} ({d['comp_group']} +{d['comp_time']})"
            rank_str = f"{d['rank']}/{d['completions']}"
            print(f"{d['mapname'][:20]:20} | {group_time_comp:32} | {rank_str:9} | Points: {d['points']} {d['comp_pts']}")


def stimeall(args):
    """stimeall [tempusid] (group) | Displays all of a player's soldier times in the specified group, or all times if group is omitted."""
    if len(args) == 0:
        print('Invalid number of arguments.')
        return
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
                print(f"{d['mapname'][:20]:20} | {group_time_comp:32} | {rank_str:9} | Points: {d['points']} {d['comp_pts']}")
        else:
            d = stime((uid, run), p=p, p2=p2, silent=True, raw=True)
            group_time_comp = f"{d['group_str']} @ {d['time_str']} ({d['comp_group']} +{d['comp_time']})"
            rank_str = f"{d['rank']}/{d['completions']}"
            print(f"{d['mapname'][:20]:20} | {group_time_comp:32} | {rank_str:9} | Points: {d['points']} {d['comp_pts']}")


def id(args):
    """id [name] | Displays all players that match the searched name and their tempus id."""
    if len(args) < 1:
        print('USAGE: id [playername]')
        return
    name = ' '.join(args)
    p = utils.get_latest_profiles()
    foundids = []
    for id in p:
        if p[id]['name'].lower().startswith(name.lower()) and id not in foundids:
            foundids.append(id)
    for id in p:
        if name.lower() in p[id]['name'].lower() and id not in foundids:
            foundids.append(id)
    for id in foundids[:50]:
        print(f'{p[id]["name"]}: {id}')

def update(args):
    """update (mapname) | Calculates points and rankings for each player from the downloaded map data.
    Optional mapname argument will only recalculate points for the given map."""
    if len(args) > 0:
        mn = utils.find_map(args[0])
        if mn is None:
            print('Map not found.')
            return
        print(f'Updating {mn} points data...')
        profiles.update_profiles(mn)
        print('Tempus data updated.')
    else:
        print('Updating all profiles...')
        profiles.build_profiles()
        print('Tempus data updated.')

def newplayers(args):
    """newplayers | Lists players that got their first run since last data"""
    p = utils.get_latest_profiles()
    p2 = utils.get_latest_profiles(x=1)
    if p2 is None:
        print('Error: No past data, everyone is a new player.')
        return
    newbies = []
    for pid in p:
        if pid not in p2:
            newbies.append(pid)
    if len(newbies) == 0:
        print('No new players since last time.')
        return
    newsoldiers = 0
    newdemos = 0
    for pid in newbies:
        if p[pid]['rank']['demoman'] != -1:
            newdemos += 1
        if p[pid]['rank']['soldier'] != -1:
            newsoldiers += 1
    print(f'{len(newbies)} new players since {utils.get_latest_profile_date(x=1)}:')
    print(f'({newsoldiers} soldiers, {newdemos} demos)')
    for pid in sorted(newbies, key=lambda x: p[x]['points']['soldier'] + p[x]['points']['demoman'], reverse=True):
        name = p[pid]['name']
        drank = p[pid]['rank']['demoman']
        dpoints = int(p[pid]['points']['demoman'])
        srank = p[pid]['rank']['soldier']
        spoints = int(p[pid]['points']['soldier'])
        if drank != -1 and srank != -1:
            print(f'{name} ({pid}) | Rank {srank} soldier ({spoints} pts) | Rank {drank} demoman ({dpoints} pts)')
        elif drank != -1:
            print(f'{name} ({pid}) | Rank {drank} demoman ({dpoints} pts)')
        elif srank != -1:
            print(f'{name} ({pid}) | Rank {srank} soldier ({spoints} pts)')
