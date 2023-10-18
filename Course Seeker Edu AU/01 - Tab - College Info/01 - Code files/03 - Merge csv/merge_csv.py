import os
from CommonLib_version_02 import create_csv, pd
course_csv_path = r'F:\Course Seeker Edu AU\Course Seeker Edu AU\00 - Tab - Course\02 - CSV files\03 - Clean data\Final_Course_data.csv'
college_info_csv_path = r'F:\Course Seeker Edu AU\Course Seeker Edu AU\01 - Tab - College Info\02 - CSV files\01 - Saved urls\College_informations.csv'
course_csv = pd.read_csv(course_csv_path)
college_info = pd.read_csv(college_info_csv_path)

course_data_dict = {'College name': [], 'Institution code': []}
for index, course_data in course_csv.iterrows():
    college_name = course_data['College name']
    institution_code = course_data['Institution Code']
    if college_name not in course_data_dict['College name']:
        course_data_dict['College name'].append(college_name)
        course_data_dict['Institution code'].append(institution_code)
temp = []
for index, course_data_2 in pd.DataFrame(course_data_dict).iterrows():
    outside_college_name = course_data_2['College name']
    outside_institution_code = course_data_2['Institution code']
    count = 0
    for index, college_info in course_csv.iterrows():
        inside_college_name = college_info['College name']
        course_id = college_info['Course ID']
        course_name = college_info['Course name']
        campus_name = college_info['Campus name']
        course_url = college_info['Course url']
        total_students = college_info['Total students']
        institution_code = college_info['Institution Code']

        if outside_college_name == inside_college_name:
            if course_id not in temp:
                temp.append(course_id)
                if not pd.isna(total_students):
                    if '<' not in total_students:
                        count += int(total_students)
                        print(course_url)
    print(outside_institution_code, '---' ,outside_college_name, '---', count)
#     df = {'College name': [outside_college_name], 'Course total students': [count], 'Institution code': [outside_institution_code]}
#     create_csv(df=pd.DataFrame(df), file_name='Course_total_students_count.csv')
#
# college_info_2 = pd.read_csv('Course_total_students_count.csv')
# merge_data = pd.merge(college_info, college_info_2, left_on='College name', right_on='College name', suffixes=('_left', '_right'), how='outer')
# merge_data.to_csv('Final_college_total_students_data.csv', index=False)
# os.remove('Course_total_students_count.csv')