import json
from CommonLib_version_01 import Commonlib, os, create_csv, requests

import pandas as pd


class Fetch_url:
    def course_url(self):
        response = requests.post(url=API_URL, headers=API_HEADER, json=PAYLOAD).text
        with open('All_course_overview.json', 'w', encoding='utf-8') as f:
            f.write(response)

        for single_course_data in json.loads(response)['hits']['hits']:
            course_api_url = 'https://www.courseseeker.edu.au/search-engine/courses/course/' + single_course_data['_id']
            # API URL: https://www.courseseeker.edu.au/search-engine/courses/course/UACADM0006
            print(course_api_url)
            create_csv(df=pd.DataFrame({'Course api url': [course_api_url]}), file_name='Courses_api_urls.csv')


if __name__ == '__main__':
    # THIS URL HAVE ALL COURSE API ID
    API_HEADER = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "1180",
        "Content-Type": "application/json",
        "Cookie": "_gid=GA1.3.2039045235.1697006426; monsido=6E11697006426480; _hjSessionUser_1526107=eyJpZCI6IjdkOTY7...",
        "Host": "www.courseseeker.edu.au",
        "Origin": "https://www.courseseeker.edu.au",
        "Referer": "https://www.courseseeker.edu.au/courses",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    API_URL = 'https://www.courseseeker.edu.au/search-engine/courses/course/_search'
    PAYLOAD = {"_source": ["name", "levelOfQualificationDesc", "admissionCentre", "institutionName", "duration",
                           "lowestRankUnadjusted", "lowestRankAdjusted", "courseCodeTac", "campuses", "applicationMode",
                           "atarProfile", "attendanceModes", "studyModes", "institution", "courseCategory"], "query": {
        "bool": {"should": [{"match_all": {}}],
                 "_name": "{\"course_search\":{\"keywords\":\"\",\"filters\":[],\"admissionCriteria\":{\"selected\":null,\"atarmin\":30,\"atarmax\":99.95},\"sortMethod\":\"relevance\",\"locality\":null,\"filterDuration\":[]},\"ip\":\"103.114.209.107\"}"}},
               "aggs": {"states": {"terms": {"field": "states", "size": 9850}},
                        "hasActiveOffering": {"terms": {"field": "hasActiveOffering", "size": 9850}},
                        "courseCategory": {"terms": {"field": "courseCategory", "size": 9850}},
                        "studyModes": {"terms": {"field": "studyModes.keyword", "size": 9850}},
                        "attendanceModes": {"terms": {"field": "attendanceModes.keyword", "size": 9850}},
                        "levelOfQualification": {"terms": {"field": "levelOfQualification", "size": 9850}},
                        "studyAreaCode": {"terms": {"field": "studyAreaCode", "size": 9850}},
                        "isUniversity": {"terms": {"field": "isUniversity", "size": 9850}},
                        "institution": {"terms": {"field": "institution", "size": 9850}}}, "size": 9850,
               "sort": ["_score", "name.keyword"]}
    obj = Fetch_url()
    obj.course_url()
