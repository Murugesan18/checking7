import datetime
import multiprocessing
import time
from CommonLib_version_02 import os, pd, Checking_Process, Commonlib, Command_line_arg, BeautifulSoup, save_html_file
from concurrent.futures import ThreadPoolExecutor
import requests


def get_soup(values):
    url = values['url']
    file_name = values['file name']
    header = values['header']
    college_name = values['College name']
    response = requests.get(url=url, headers=header)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        new_tag = soup.new_tag('college')
        new_tag['url'] = url
        new_tag.string = college_name
        body_tag = soup.body
        body_tag.insert(0, new_tag)
        save_html_file(soup=soup, file_name=file_name, operation=operation, url=url)
        print('Successfully saved url...', url)
    else:
        print('Wrong status code url is...', url)
if __name__ == '__main__':
    description = 'Save institutions Url'
    epilog = '''Usage: py save_institutions_url.py -file_name FILENAME -path PATH -operation OPERATION'''
    file_name_help = 'Give already collected institutions url csv file name Example: "Study_australia_institutions_urls.csv"'
    path_help = r'Give saved university url csv file path Example: "F:\Course Seeker Edu AU\Course Seeker Edu AU\00 - Tab - Course\02 - CSV files\01 - Saved urls"'
    operation_help = 'Give Save institutions page operation name Example: "Save institutions url"'

    # args = Command_line_arg(description=description, epilog=epilog, file_name=True, path=True, operation=True, file_name_help=file_name_help, path_help=path_help, operation_help=operation_help)
    # csv_file_path = args.path
    # csv_file_name = csv_file_path + fr'\{args.file_name}'
    # operation = args.operation

    csv_file_path = r'F:\Course Seeker Edu AU\Course Seeker Edu AU\01 - Tab - College Info\02 - CSV files\01 - Saved urls'
    csv_file_name = csv_file_path + r'\Institutions_urls.csv'
    operation = 'Save institutions url'

    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "_gid=GA1.3.2039045235.1697006426; monsido=6E11697006426480; _hjSessionUser_1526107=eyJpZCI6IjdkOTY3ZjlhLWFmZTMtNWVhMi1hNzk1LTg2YzQyNThmNWI2YSIsImNyZWF0ZWQiOjE2OTcwMDY0MjU9NzQsImV4aXN0aW5nIjp0cnVlfQ==; _ga_X2FSJ6R6VC=deleted; _hjSession_1526107=eyJpZCI6ImNmNmVlZWFlLTNlMjAtNDgxNS1iMGY0LWE3MDEzY2AFTlNGE6MiIsImNyZWF0ZWQiOjE2OTcxNjk0NTUwNTIsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6dHJ1ZX0=; _hjAbsoluteSessionInProgress=0; _hjIncludedInSessionSample_1526107=0; _ga_X2FSJ6R6VC=deleted; _gat_gtag_UA_127168367_1=1; _ga=GA1.1.590713196.1697006426; _ga_X2FSJ6R6VC=GS1.1.1697169454.9.1.1697174494.0.0.0",
        "Host": "www.courseseeker.edu.au",
        "Referer": "https://www.courseseeker.edu.au/institutions?state=",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    checking_process_obj = Checking_Process()
    visited_file_list = checking_process_obj.check_visited_html_file(operation)

    valid_url_list = []
    for index, valid_url in pd.read_csv(csv_file_name).iterrows():
        college_name = valid_url['College name']
        valid_url = valid_url['url']
        file_name = valid_url.split('/')[-1].replace('=', '_')
        print(file_name)
        if file_name in visited_file_list:
            print('Already saved...', valid_url)
            print('Index: ', index)
        else:
            values = {'url': valid_url, 'file name': file_name, 'header': header, 'College name': college_name}
            valid_url_list.append(values)

    try:
        max_worker = multiprocessing.cpu_count()
    except:
        max_worker = 3

    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        executor.map(get_soup, valid_url_list)
