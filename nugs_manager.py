import requests


nugs_aqueous_search_json = 'http://nugs.net/api.aspx?orgn=nnsite&method=catalog.search&searchStr=aqueous'


def get_search_json() -> dict:
    r = requests.get(nugs_aqueous_search_json)
    return r.json()


def nugs_recording_url(date: str) -> str:
    date_parts = [str(int(part)) for part in date.split('-')]
    formatted_date = '/'.join([date_parts[1], date_parts[2], date_parts[0]])
    print(formatted_date)
    nugs_json = get_search_json()
    search_results = nugs_json['Response']['catalogSearchTypeContainers'][0]['catalogSearchContainers'][0]['catalogSearchResultItems']

    filtered_json = filter(lambda result: result['performanceDate'] == formatted_date, search_results)

    try:
        return 'http://nugs.net' + next(filtered_json)['pageURL']
    except StopIteration:
        return ''
