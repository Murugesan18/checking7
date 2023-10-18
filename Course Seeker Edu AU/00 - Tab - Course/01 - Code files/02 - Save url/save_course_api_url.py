import multiprocessing
from CommonLib_version_02 import os, pd, Checking_Process, Commonlib, Command_line_arg, clean_header
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    description = 'Save course api Url'
    epilog = '''Usage: py save_course_api_url.py -file_name FILENAME -path PATH -operation OPERATION'''
    file_name_help = 'Give already collected course api url csv file name Example: "Study_australia_course_api_urls.csv"'
    path_help = r'Give saved university url csv file path Example: "F:\Course Seeker Edu AU\Course Seeker Edu AU\00 - Tab - Course\02 - CSV files\01 - Saved urls"'
    operation_help = 'Give Save course api page operation name Example: "Save course api url"'

    # args = Command_line_arg(description=description, epilog=epilog, file_name=True, path=True, operation=True, file_name_help=file_name_help, path_help=path_help, operation_help=operation_help)
    # csv_file_path = args.path
    # csv_file_name = csv_file_path + fr'\{args.file_name}'
    # operation = args.operation

    csv_file_path = r'F:\Course Seeker Edu AU\Course Seeker Edu AU\00 - Tab - Course\02 - CSV files\01 - Saved urls'
    csv_file_name = csv_file_path + r'\Courses_api_urls.csv'
    operation = 'Save course api url'

    header = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "_gid=GA1.3.2039045235.1697006426; monsido=6E11697006426480; _hjSessionUser_1526107=eyJpZCI6IjdkOTY7...",
    "Host": "www.courseseeker.edu.au",
    # "Referer": "https://www.courseseeker.edu.au/courses/advanced-diploma-of-bible-mission-and-ministry-UACADM0006",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

    checking_process_obj = Checking_Process()
    visited_file_list = checking_process_obj.check_visited_json_file(operation)

    common_lib = Commonlib(continuous_count=1, operation=operation, time_delay=0)
    valid_url_list = []
    for index, valid_url in pd.read_csv(csv_file_name).iterrows():
        valid_url = valid_url['Course api url']
        file_name = valid_url.split('/')[-1].replace('=', '_')
        print(file_name)
        if file_name in visited_file_list:
            print('Already saved...', valid_url)
            print('Index: ', index)
        else:
            values = {'url': valid_url, 'file name': file_name, 'header': header, 'file type': 'json'}
            valid_url_list.append(values)
        # if index == 1000:
        #     break


    try:
        max_worker = multiprocessing.cpu_count()
    except:
        max_worker = 3

    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        executor.map(common_lib.save_data_use_request, valid_url_list)