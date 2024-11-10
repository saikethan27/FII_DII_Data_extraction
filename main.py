import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from get_month_end_date import generate_last_days

# The URL of the page you want to scrape

def get_data_main(url,date):
    cookies = {
        'csrftoken': 'gFKduF5xSnQpRRYsx4xlFY9tdTfPKBsiPeOzazyVYTYyaFruUNBK4ky7ZyRF1EA6',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'csrftoken=gFKduF5xSnQpRRYsx4xlFY9tdTfPKBsiPeOzazyVYTYyaFruUNBK4ky7ZyRF1EA6',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    # Define a function to extract data from a specific tab
    def extract_tab_data(tab_id):
        tab_data = []
        tab_content = soup.find('div', id=tab_id)
        
        if tab_content:
            table1 = tab_content.find_all('table')
                    # Extract the JSON data from data-jsondata attribute

            i=0
            for table in table1:
                i+=1
                json_data = table['data-jsondata']
                parsed_data = json.loads(json_data)
                
                # Extract headers and data from the parsed JSON
                headers = parsed_data.get('headers', [])
                tab_data = parsed_data.get('data', [])
                # Format and print headers
                header_str = '\n'.join(headers)
                print("header= '")
                print(header_str)
                print("'")


                del tab_data[0:3]
                #     print(d)
                # print(data)
                # if table:
                #     headers = [th.get_text(strip=True) for th in table.find_all('th')]
                #     rows = table.find_all('tr')[1:]  # Skip header row
                    
                #     for row in rows:
                #         cols = row.find_all('td')
                #         if cols:
                #             tab_data.append([col.get_text(strip=True) for col in cols])
                df=pd.DataFrame(tab_data,columns=headers)
                # Path to the CSV file
                csv_file_path = tab_id+'_'+str(i)

                # Check if the CSV file exists
                if os.path.exists(csv_file_path):
                    # If it exists, append the DataFrame to the CSV file without writing the header
                    df.to_csv(csv_file_path, mode='a', header=False, index=False)
                else:
                    # If it does not exist, create a new CSV file with headers
                    df.to_csv(csv_file_path, mode='w', header=True, index=False)

                print(f'Data has been {"appended to" if os.path.exists(csv_file_path) else "written to"} {csv_file_path}.')
                print("\n" + "="*40 + "\n")

        return header_str, tab_data

    # List of tab IDs corresponding to the required tabs
    tab_ids = [
        'Snapshot_modal',  # Summary
        'Cash_modal',      # Cash Provisional
        'FII_modal',
        # 'fii-index-modal-modal-pastmonth',
        # 'fii-stock-modal-modal-pastmonth',       # FII Cash
        'FNO_modal',       # FII F&O
        'MF_modal', 
        # 'mf-index-modal-pastmonth',       # MF Cash
        # 'mf-stock-modal-pastmonth',
        'MF_FNO_modal'     # MF F&O
    ]

    # Extract data from each tab
    for tab_id in tab_ids:
        try:
            headers, data = extract_tab_data(tab_id)
            print(f"Data from {tab_id}:")
            print("Headers:", headers)
        except Exception as e:
            print(f"Error extracting data from {tab_id}: {str(e)}")
            with open('error.txt','a') as error_file:
                error_file.write(f"Error extracting data from url {url} tab_id {tab_id} date{date}: {str(e)}\n ")
  
all_dates=generate_last_days()  
 
for date in all_dates:
    url = f'https://trendlyne.com/macro-data/fii-dii-month/snapshot/{date}'  # Replace with the actual URL
    get_data_main(url,date)
    print(f'date -- {date}')