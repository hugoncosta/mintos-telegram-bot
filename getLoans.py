import requests
import pandas as pd

# load dbs
LO_db = pd.read_csv("LO_db.csv")
user_db = pd.read_csv("user_db.csv")


def getPMloans(code):
    data = {'lender_groups[]': code,
            'currencies[]': '978',
            'with_buyback': '1',
            'max_results': '20',
            'sort_field': 'interest',
            'sort_order': 'DESC',
            'format': 'json'
            }
    response = requests.post('https://www.mintos.com/webapp/api/en/market/primary/list', data=data)
    try:
        return response.json()["data"]["list"][3]["loan_rate_percent"][:4]+'%'
    except:
        return 'No PM Loans'


def getSMloans(code):
    data = {'lender_groups[]': code,
            'max_premium': '0.0',
            'statuses^[^]': '256',
            'currencies^[^]': '978',
            'with_buyback': '1',
            'max_results': '20',
            'sort_field': 'ytm',
            'sort_order': 'DESC',
            'page': '1',
            'format': 'json'
            }
    response = requests.post('https://www.mintos.com/webapp/api/en/market/secondary/list', data=data)
    try:
        return response.json()["data"]["list"][3]["yield_to_maturity"][:4]+'%'
    except:
        return 'No SM Loans'
    

def getLoans(chosenLOs):
    df = LO_db[LO_db.LO.isin(chosenLOs)]
    pm_interests = []
    sm_interests = []

    for LO in df['Code']:
        pm_interests.append(getPMloans(LO))
        sm_interests.append(getSMloans(LO))

    df['PM Interest'] = pm_interests
    df['SM Interest'] = sm_interests
    return df.drop('Code', axis=1).to_markdown(showindex=False)

if __name__ == '__main__':
    print('Testing for Mogo')
    getLoans([2])