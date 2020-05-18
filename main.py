from requests import get
import json
import datetime
import time

BASE_URL = 'https://api.esportal.com/tournament/get?_=1579280233646&id={camp_id}'
BASE_URL_TEAM = 'https://api.esportal.com/team/get?_=1579290242888&slug={slug_name}&users=1&activities=0'
BASE_MATCH_URL = "https://api.esportal.com/tournament/match/get?_=1579293384440&match_id={match_id}"
BASE_PLAYER_URL = "https://api.esportal.com/user_profile/get?_=1580507874271&id={player_id}"
tournaments = range(280,331)


def make_tournament_request_url(tournaments_ids):
    print('----------------------------------')
    urls = []
    for camp_id in tournaments_ids:    
        print(f'Montando url do camp {camp_id}')
        camp_url = BASE_URL.format(camp_id=camp_id)
        urls.append(camp_url)
    return urls

def request_tournament(tournament_request_urls):
    teams_names = []
    for url in tournament_request_urls:
        # time.sleep(5)
        returned_json = get(url).text
        print(returned_json)
        if url.split("=")[-1] not in ["303"]:
            parsed = json.loads(returned_json)
        tourn_name = parsed["name"]
        print(f'Request feito em: {url}')
        print(f'Torneio: {tourn_name}')

        if 'TUES' in tourn_name:
            for team in parsed['teams']:
                teams_names.append(team['slug_name'])
            return teams_names
        else:
            return None
    return None


def make_team_request_url(slug_name):
    return BASE_URL_TEAM.format(slug_name=slug_name)


def request_team_members(team_request_url):
    player_names = []
    # time.sleep(5)
    returned_json = get(team_request_url).text
    parsed = json.loads(returned_json)
    team_members = parsed['members']
    print(f'Request feito em: {team_request_url}')
    for player in team_members:
        player_id = player['id']
        player_username = player['username']
        print(f'Player: {player_username}')
        print(f'playerid32: {player_id}')

    print('----------------------------------')

def request_camp_matches(tournament_request_urls):
    camp_matches = []
    for url in tournament_request_urls: 
        # time.sleep(5)    
        returned_json = get(url).text
        print(type(returned_json), "->",url.split("=")[-1], "!")
        if url.split("=")[-1] not in ["303", "305", "325"]:
            parsed = json.loads(returned_json)
        tourn_name = parsed["name"]
        print(f'Request feito em: {url}')
        print(f'Torneio: {tourn_name}') 
        matches = parsed['matches']
        # print(matches)
        if 'TUES' in tourn_name and matches is not None:
            match_ids = [each['id'] for each in matches]
            camp_matches.append({
                "id": parsed["id"], 
                "matches": match_ids
            })
    return camp_matches

def make_request_camp_match_url(match):
    match_url = BASE_MATCH_URL.format(match_id = match)
    print(match_url)
    return match_url


def request_players_matches(camp_matches):
    players_matches = []
    for camp in camp_matches:
        matches = []
        for match in camp["matches"]:
            # time.sleep(5)
            returned_json = get(make_request_camp_match_url(match)).text
            parsed = json.loads(returned_json)
            players_ids = [player['id'] for player in parsed['players']]
            players_matches.append({'match_id': parsed['id'], 'players_on_match': players_ids})
    return players_matches

def make_request_player_url(player_id):
    return BASE_PLAYER_URL.format(player_id = player_id)

def get_playerid32(matches_players):
    all_ids = []
    playerid32 = []
    for match in matches_players:
        all_ids += match["players_on_match"]
    steamids = set(all_ids)
    # for esportal_id in ids_to_request:
    #     returned_json = get(make_request_player_url(esportal_id)).text
    #     parsed = json.loads(returned_json)
    #     playerid32.append(parsed[])


    return list(steamids)

def write_on_file(steamids):
    now = datetime.datetime.now()
    print(len(steamids))
    ids = ",".join(str(x) for x in steamids)
    with open(now.strftime("%Y-%m-%d %H:%M:%S"), "w") as f:
        f.write("(")
        f.write(ids)
        f.write(")")

if __name__ == '__main__':
    team_list = []
    links = make_tournament_request_url(tournaments)
    print(links)

    matches_ids = request_camp_matches(links)
    print(matches_ids)
    players_matches = request_players_matches(matches_ids)
    print(players_matches)
    steamids = get_playerid32(players_matches)
    write_on_file(steamids)
