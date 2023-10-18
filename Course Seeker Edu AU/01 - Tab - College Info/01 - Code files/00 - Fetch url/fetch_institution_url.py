import json
import re
from CommonLib_version_01 import Commonlib, os, create_csv, requests

import pandas as pd


class Fetch_url:
    def institution_url(self):
        response = requests.post(url=API_URL, headers=API_HEADER, json=PAYLOAD).text
        with open('All_institutions_overview.json', 'w', encoding='utf-8') as f:
            f.write(response)

        for single_course_data in json.loads(response)['hits']['hits']:
            institution_name = single_course_data['_source']['institutionName']#.replace('CG Spectrum Institution', 'CG Spectrum Institute')
            # COURSE URL
            try:
                input_string = institution_name.lower()
                if input_string[-1] == ' ':
                    print(input_string)
                    input_string = input_string.strip() + '12345'
                else:
                    input_string = input_string
                special_chars_pattern = r'[!@#$%^&*()_+={}\[\]:;"\'<>,?/\\|`~]'
                # Replace special characters with spaces
                output_string = re.sub(special_chars_pattern, ' ', input_string).replace('–', ' ').replace('—', ' ').replace('-', ' ').strip()
                college_url = 'https://www.courseseeker.edu.au/institutions/' + re.sub('\s+', '-', output_string).replace('12345', '-').replace('bbi-the-australian', 'bbi---the-australian')
                # create_csv(df=pd.DataFrame({'url': [college_url], 'College name': [institution_name]}), file_name='Institutions_urls.csv')
                print(college_url)
            except:
                course_url = ''


if __name__ == '__main__':
    # THIS URL HAVE ALL COURSE API ID
    API_HEADER = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "1074",
        "Content-Type": "application/json",
        "Cookie": "_gid=GA1.3.2039045235.1697006426; monsido=6E11697006426480; _hjSessionUser_1526107=eyJpZCI6IjdkOTY3ZjlhLWFmZTMtNWVhMi1hNzk1LTg2YcQyNThmNWI2YSIsImNyZWF0ZWQiOjE2OTcwMDY0MjU5NzQsImV4aXN0aW5nIjp0cnVlfQ==; _ga_X2FSJ6R6VC=deleted; _hjIncludedInSessionSample_1526107=0; _hjAbsoluteSessionInProgress=0; _ga_X2FSJ6R6VC=deleted; _hjSession_1526107=eyJpZCI6IjNiM2JkODc0LTY4MjgtNGIwMS05YmJmLWJiN2JhNWE5ZmU5MiIsImNyZWF0ZWQiOjE2OTcxMDAwMTExMDQsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6dHJ1ZX0=; _ga=GA1.1.590713196.1697006426; _ga_X2FSJ6R6VC=GS1.1.1697099601.7.1.1697103376.0.0.0",
        "Host": "www.courseseeker.edu.au",
        "Origin": "https://www.courseseeker.edu.au",
        "Referer": "https://www.courseseeker.edu.au/institutions?state=",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    API_URL = 'https://www.courseseeker.edu.au/search-engine/courses%2Cinstitutions/course%2Cinstitution/_search'
    PAYLOAD = {"_source": ["institution", "institutionName"], "query": {"bool": {
        "should": [{"bool": {"must": [{"term": {"_index": "courses*"}}]}},
                   {"bool": {"must": [{"term": {"_index": "institutions*"}}]}}]}}, "aggs": {
        "institutionWash": {"aggs": {"institution": {"terms": {"field": "institution", "size": 200}}},
                            "filter": {"bool": {"must": [{"term": {"_index": "courses*"}}]}}}, "states": {"aggs": {
            "states": {"terms": {"field": "states", "size": 200},
                       "aggs": {"institution": {"terms": {"field": "institution", "size": 200}}}}}, "filter": {
            "bool": {"must": [{"term": {"_index": "courses*"}}]}}}, "studyAreaCode": {"aggs": {
            "studyAreaCode": {"terms": {"field": "studyAreaCode", "size": 200},
                              "aggs": {"institution": {"terms": {"field": "institution", "size": 200}}}}}, "filter": {
            "bool": {"must": [{"term": {"_index": "courses*"}}]}}}, "isUniversity": {"aggs": {
            "isUniversity": {"terms": {"field": "isUniversity", "size": 200},
                             "aggs": {"institution": {"terms": {"field": "institution", "size": 200}}}}}, "filter": {
            "bool": {"must": [{"term": {"_index": "courses*"}}]}}}},
               "post_filter": {"term": {"_index": "institutions*"}}, "size": 200,
               "sort": ["_score", "institutionName.keyword"]}
    obj = Fetch_url()
    obj.institution_url()
