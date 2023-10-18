import re
from CommonLib_version_02 import pd, os, create_csv, Checking_Process, Command_line_arg, read_json_files, create_log, BeautifulSoup, clear_text
import inspect

import requests


class Course_data:
    check_box = []
    def replace_unwanted_text(self, value, atar_profile):
        if value is not None:
            value = value
            if re.search('[A-z]', value):
                message = atar_profile['message']
                df = {'Alphabetical value': [value], 'Message': [message]}
                create_csv(df=pd.DataFrame(df), file_name='Alphabetical_value_messages.csv')
            value = value.replace('N/P', '').replace('L/N', '').replace('N/A', '').replace('NC', '').replace('NO', '').replace('NA', '')

        else:
            value = value
        return value

    def get_data(self):
        count = 1
        for files in os.listdir(html_files_path):
            data = read_json_files(file_name=files, folder_path=html_files_path, line_num=inspect.currentframe().f_lineno, visited_files=visited_files)
            if data:
                _id = data['_id']
                data = data['_source']
                # COLLEGE NAME
                try:
                    college_name = data['institutionName']
                except Exception as e:
                    print('Check college name error: ', e)
                    college_name = ''

                # COLLEGE URL
                try:
                    input_string = college_name.lower()
                    special_chars_pattern = r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~]'
                    # Replace special characters with spaces
                    output_string = re.sub(special_chars_pattern, ' ', input_string).replace('–', ' ').replace('—', ' ').replace('-', ' ').strip()
                    college_url = 'https://www.courseseeker.edu.au/institutions/' + re.sub('\s+', '-', output_string)
                except Exception as e:
                    print('Check college url error: ', e)
                    college_url = ''

                # COURSE NAME
                try:
                    course_name = data['name'].strip()
                except Exception as e:
                    print('Check course name error: ', e)
                    course_name = ''

                # COURSE URL
                try:
                    input_string = course_name.lower()
                    special_chars_pattern = r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~]'
                    # Replace special characters with spaces
                    output_string = re.sub(special_chars_pattern, ' ', input_string).replace('–', ' ').replace('—', ' ').replace('-', ' ').strip()
                    course_url = 'https://www.courseseeker.edu.au/courses/' + re.sub('\s+', '-', output_string) + '-' + _id
                except:
                    course_url = ''

                # STUDENT PROFILE
                try:
                    intake_year = data['studentProfile']['collectionYear']
                    total_students = data['studentProfile']['totalStudents']
                    total_students = self.replace_unwanted_text(total_students, data['studentProfile'])
                except Exception as e:
                    intake_year, total_students = '', ''
                    print('Check student profile error: ', e, course_url)

                # ATAR PROFILE
                try:
                    atar_profile_key = data['atarProfile']

                    highest_rank_atar = self.replace_unwanted_text(atar_profile_key['highestAtarUnadjusted'], atar_profile_key)
                    highest_selection_rank = self.replace_unwanted_text(atar_profile_key['highestAtarAdjusted'], atar_profile_key)

                    median_rank_atar = self.replace_unwanted_text(atar_profile_key['medianAtarUnadjusted'], atar_profile_key)
                    median_selection_rank = self.replace_unwanted_text(atar_profile_key['medianAtarAdjusted'], atar_profile_key)

                    lowest_rank_atar = self.replace_unwanted_text(atar_profile_key['lowestAtarUnadjusted'], atar_profile_key)
                    lowest_selection_rank = self.replace_unwanted_text(atar_profile_key['lowestAtarAdjusted'], atar_profile_key)
                except Exception as e:
                    highest_rank_atar, median_rank_atar, lowest_rank_atar = '', '', ''
                    highest_selection_rank, median_selection_rank, lowest_selection_rank = '', '', ''
                    print('Check atar profile error: ', e, course_url)

                # CAMPUS DETAILS
                try:
                    for single_campus in data['campuses']:
                        campus_name = single_campus['campusName']
                        campus_id = single_campus['campusCode']
                        campus_code = campus_id.split('-')[-1]
                        institution_code = campus_id.split('-')[0]

                        if 'geolocation' in single_campus:
                            latitude = single_campus['geolocation']['lat']
                            longitude = single_campus['geolocation']['lon']
                        else:
                            latitude, longitude = '', ''
                        df = {'College name': [college_name], 'College url': [college_url], 'Course name': [course_name],
                              'Course url': [course_url], 'Course ID': [_id],
                              'Highest rank to receive an offer - ATAR': [highest_rank_atar],
                              'Median rank to receive an offer - ATAR': [median_rank_atar],
                              'Lowest rank to receive an offer - ATAR': [lowest_rank_atar],
                              'Highest rank to receive an offer - Selection Rank': [highest_selection_rank],
                              'Median rank to receive an offer - Selection Rank': [median_selection_rank],
                              'Lowest rank to receive an offer - Selection Rank': [lowest_selection_rank],
                              'Campus name': [campus_name], 'Campus latitude': [latitude],
                              'Campus longitude': [longitude], 'Intake year': [intake_year],
                              'Total students': [total_students], 'Campus ID': [campus_id],
                              'Campus Code': [campus_code], 'Institution Code': [institution_code]}
                        create_csv(df=pd.DataFrame(df), file_name='Final_Course_data.csv')
                        print(count, course_url)
                except Exception as e:
                    print('Check campus data: ', e, course_url)
                count += 1

            # create_csv(df=pd.DataFrame({'file name': [files]}), file_name=visited_file_csv_name)

if __name__ == '__main__':
    description = 'Get Course data'
    epilog = '''Usage: py fetch_course_data.py -path PATH -operation OPERATION'''
    path_help = r'Give saved universities url HTML file path Example: "F:\Course Seeker Edu AU\Course Seeker Edu AU\00 - Tab - Course\01 - Code files\02 - Save url\Save course api url Html"'
    operation_help = 'Give Get Course data operation name Example: "Get Course data"'

    # args = Command_line_arg(description=description, epilog=epilog, file_name=False, path=True, operation=True,
    #                         path_help=path_help, operation_help=operation_help)

    # html_files_path = args.path
    # operation = args.operation

    html_files_path = r'F:\Course Seeker Edu AU\Course Seeker Edu AU\00 - Tab - Course\00 - Saved pages\00 - JSON files\Courses JSON files'
    operation = 'Get Course data'

    visited_file_csv_name = 'course_visited_file.csv'
    checking_process_obj = Checking_Process()
    visited_files = checking_process_obj.check_visited_url(visited_file_csv_name)

    course_data_obj = Course_data()
    course_data_obj.get_data()