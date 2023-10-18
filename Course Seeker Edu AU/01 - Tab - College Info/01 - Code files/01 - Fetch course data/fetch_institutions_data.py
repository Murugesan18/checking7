import re
from CommonLib_version_02 import pd, os, create_csv, Checking_Process, Command_line_arg, read_html_files, create_log, BeautifulSoup, clear_text
import inspect

class Institutions_data:
    def replace_unwanted_text(self, value):
        if value is not None:
            value = value.replace('N/P', '').replace('L/N', '')
        else:
            value = value
        return value

    def get_data(self):
        for files in os.listdir(html_files_path):
            data = read_html_files(file_name=files, folder_path=html_files_path, line_num=inspect.currentframe().f_lineno, visited_files=visited_files)
            if data:
                # COLLEGE NAME AND URL
                try:
                    college_name = data.find('college').text
                    college_url = data.find('college')['url']
                except Exception as e:
                    print('Check college name error: ', e)
                    college_name, college_url = '', ''
                print(college_url)
                estd_year = ''
                institution_about = data.find('div', id='institution-profile-about')
                if 'since' in str(institution_about):
                    if re.search('(since|established in)\s\d{4}', str(institution_about)):
                        estd_year = re.search('(since|established in)\s(\d{4})', str(institution_about)).group(2)

                if data.find('table', class_='student-profile-table'):
                    table_tag = data.find('table', class_='student-profile-table')
                    # college_intake_year = re.search('\d{4}', str(table_tag.find('thead').find('tr'))).group()
                    total_students = table_tag.find('tr', class_='total').find('td').text.strip()
                else:
                    total_students = ''

                df = {'College name': [college_name], 'College url': [college_url], 'Establishment year': [estd_year],
                      'Total students': [total_students]}
                create_csv(df=pd.DataFrame(df), file_name='College_informations.csv')
            create_csv(df=pd.DataFrame({'file name': [files]}), file_name=visited_file_csv_name)

if __name__ == '__main__':
    description = 'Get Institutions data'
    epilog = '''Usage: py fetch_institutions_data.py -path PATH -operation OPERATION'''
    path_help = r'Give saved universities url HTML file path Example: "F:\Course Seeker Edu AU\Course Seeker Edu AU\01 - Tab - College Info\00 - Saved pages\HTML files\Institutions url Html"'
    operation_help = 'Give Get Institutions data operation name Example: "Get Institutions data"'

    # args = Command_line_arg(description=description, epilog=epilog, file_name=False, path=True, operation=True,
    #                         path_help=path_help, operation_help=operation_help)

    # html_files_path = args.path
    # operation = args.operation

    html_files_path = r'F:\Course Seeker Edu AU\Course Seeker Edu AU\01 - Tab - College Info\00 - Saved pages\HTML files\Institutions url Html'
    operation = 'Get Institutions data'

    visited_file_csv_name = 'institutions_visited_file.csv'
    checking_process_obj = Checking_Process()
    visited_files = checking_process_obj.check_visited_url(visited_file_csv_name)

    course_data_obj = Institutions_data()
    course_data_obj.get_data()