import requests
from bs4 import BeautifulSoup
import pandas as pd


# # pasting the url of the website after searching for keywords if needed # i.e. url =
# 'https://grand-challenge.org/aiforradiology/?subspeciality=All&modality=All&ce_under=All&ce_class=All&fda_class=All
# &sort_by=last+modified&search=cancer'

url = 'https://grand-challenge.org/aiforradiology/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

boxes = soup.select('div.row.py-4.border-top')
results = []

for box in boxes:
    product = box.select_one('div.h3.font-weight-bold.mb-1 > a')
    purpose = box.select_one('div.text-muted > p')
    company = box.select_one('div.h6.pb-2 > a')
    description = box.select_one('p:not(.text-muted)')

    subspeciality = box.select_one('div.h6 > span:nth-of-type(2)')
    modality = box.select_one('div.h6 > span:nth-of-type(4)')

    ce_value = box.select_one('div.pr-2 > a:nth-child(1)')

    info_source = box.select_one('span.h6.text-muted:contains("Information source:") + div')
    cert_verified = box.select_one('span.h6.text-muted:contains("Certification verified:") + div')

    item = {
        'Product': product.text.strip() if product else None,
        'Purpose': purpose.text.strip() if purpose else None,
        'Company': company.text.strip() if company else None,
        'Description': description.text.strip() if description else None,
        'Subspeciality': subspeciality.text.strip() if subspeciality else None,
        'Modality': modality.text.strip() if modality else None,
        'CE': ce_value.text.strip() if ce_value else None,
        'Information_source': info_source.text.strip() if info_source else None,
        'Certification_verified': cert_verified.text.strip() if cert_verified else None
    }

    results.append(item)

df = pd.DataFrame(results)
print(df)

df.to_excel('/path/to/file.xlsx')