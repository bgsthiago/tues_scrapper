from requests import get
import json

BASE_URL = 'https://api.esportal.com/tournament/get?_=1579280233646&id={camp_id}'
BASE_URL_TEAM = 'https://api.esportal.com/team/get?_=1579290242888&slug={slug_name}&users=1&activities=0'
tournaments = range(280, 330)


def make_tournament_request_url(camp_id):
    print('----------------------------------')
    print(f'Montando url do camp {camp_id}')
    return BASE_URL.format(camp_id=camp_id)


def request_tournament(tournament_request_url):
    teams_names = []
    returned_json = get(tournament_request_url).text
    parsed = json.loads(returned_json)
    tourn_name = parsed["name"]
    print(f'Request feito em: {tournament_request_url}')
    print(f'Torneio: {tourn_name}')

    if 'TUES' in tourn_name:
        for team in parsed['teams']:
            teams_names.append(team['slug_name'])
        return teams_names
    else:
        return None


def make_team_request_url(slug_name):
    return BASE_URL_TEAM.format(slug_name=slug_name)


def request_team_members(team_request_url):
    player_names = []
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


if __name__ == '__main__':
    team_list = []
    link = make_tournament_request_url(319)
    returned_teams = request_tournament(link)
    if returned_teams:
        team_list.append(returned_teams)
        # print(set(returned_teams))
        # print(json.dumps(team_list[0], indent=4, sort_keys=True))
    link = make_team_request_url('santa-bronx-ufu-esports')
    request_team_members(link)

