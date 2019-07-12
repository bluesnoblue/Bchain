import requests

base_url = 'http://127.0.0.1:5000'

while True:
    r = requests.get(base_url + '/chain')
    print(r.json())
    chains = r.json()['chain']

    transaction = {
                'sender': 'Blues1',
                'recipient': 'Blues2',
                'amount': '10'}
    r = requests.post(base_url + '/transactions/new', json=transaction)
    print(r.json())

    r = requests.get(base_url + '/mine')
    print(r.json())