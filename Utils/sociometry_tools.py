# -*- coding: utf-8 -*-
import pandas as pd
import os
import xlsxwriter
import numpy as np

NUM_NUMERICALS = 13
NUM_Q_OPEN = 2


class SociometryTools:
    def __init__(self, responses_path, outputs_path):
        self._responses_path = responses_path
        self._outputs_path = outputs_path

        try:
            outputs_individual_dir = outputs_path + "חניכים" + "/"
            os.mkdir(outputs_individual_dir)
        except:
            pass

        self._outputs_combined_path = outputs_path + "גולמי מאוחר (ללא ציונים).xlsx"
        self._outputs_example_person_path = outputs_path + "חניכים" + "/{0}.xlsx"
        self._outputs_numeric_summary_path = outputs_path + "ציונים מחזורי.xlsx"
        self._outputs_means_summary_path = outputs_path + "ממוצעים וסטיות תקן.xlsx"

    def run(self):
        error = ""

        # Get all the excel files' directory inside the FILES_DIRECTORY
        excel_dirs = []
        for fn in os.listdir(self._responses_path):
            if fn.endswith('.xlsx'):
                excel_dirs.append(self._responses_path + fn)

        # Read all the excel files
        excels = [pd.ExcelFile(name) for name in excel_dirs]

        # Turn them into dataframes
        frames = [x.parse(x.sheet_names[0], header=None, index_col=None) for x in excels]

        height_width = (
            len(excel_dirs) + 2,
            NUM_NUMERICALS + NUM_Q_OPEN + 1
        )

        # (number_of_persons + 2, number of questions + 1)
        print(height_width)
        shapes = [frames[i].shape == height_width for i in range(len(frames))]

        print([frames[i].shape for i in range(len(frames))])

        if not all(shapes):
            print("Not all excels are the right size")

            # Create a workbook and add a worksheet.
            workbook = xlsxwriter.Workbook(self._outputs_combined_path)
            worksheet = workbook.add_worksheet()

            worksheet.write(0, 0, error)
            workbook.close()
            return

        # Delete the first row for all frames except the first
        # i.e. remove the header row -- assumes it's the first
        frames = [df[np.arange(len(df)) != 1] for df in frames]
        frames[1:] = [df[1:] for df in frames[1:]]

        # The amount of machzor members is the length of the first frame,
        # minus one (because of the header)
        num_machzor_members = len(frames[0][1]) - 1

        # is it really necessary?
        # # Loop over all the frames and change the names to numbers
        # for i in range(len(frames)):
        #     if i == 0:
        #         frames[i][0] = [frames[i][0][0]] + [k for k in range(1,num_machzor_members+1)]
        #         text = 'קוד אישי'
        #         frames[i].insert(1, "personal_code", [text] + ['C' + str(i) for k in range(num_machzor_members)])
        #     else:
        #         frames[i][0] = [k for k in range(1,num_machzor_members+1)]
        #         frames[i].insert(1, "personal_code", ['C' + str(i) for k in range(num_machzor_members)])

        # Concatenate all the files
        combined = pd.concat(frames)  # returns the DataFrame of the output

        # Group and sort by name
        headers = combined.iloc[0]
        combined = pd.DataFrame(combined.values[1:], columns=headers)
        combined.sort_values(by=combined.columns[0], inplace=True)

        # Write it out
        combined.to_excel(self._outputs_combined_path, header=False, index=False)

        # Calculates means ands std
        people_means = np.zeros((height_width[0] - 2, NUM_NUMERICALS))

        # Gets names of all people
        names = frames[0][0][1:].values

        # Calculate means for each person
        for i in range(len(names)):
            frame = combined[combined[combined.columns[0]].isin([names[i]])]
            person_values = [frame[frame.columns[i]].values[~pd.isnull(frame[frame.columns[i]].values)]
                             for i in range(1, 14)]

            for j in range(NUM_NUMERICALS):
                people_means[i, j] = np.mean(person_values[j])

        means = np.mean(people_means, axis=0)
        stds = np.std(people_means, axis=0)

        means_frame = pd.DataFrame(columns=combined.columns)
        means_to_print = ['ממוצע'] + means.tolist() + [None, None]
        means_to_print = {frame.columns[i]: means_to_print[i] for i in range(len(means_to_print))}
        stds_to_print = ['סטיית תקן'] + stds.tolist() + [None, None]
        stds_to_print = {frame.columns[i]: stds_to_print[i] for i in range(len(stds_to_print))}
        means_frame = means_frame.append(means_to_print, ignore_index=True)
        means_frame = means_frame.append(stds_to_print, ignore_index=True)
        self.export_to_excel(self._outputs_means_summary_path, means_frame)

        people_scores_frame = pd.DataFrame(columns=combined.columns)
        # Creates personal sheet for each person
        for k in range(len(names)):
            person = names[k]
            frame = combined[combined[combined.columns[0]].isin([person])]
            tmp = ['ממוצע רגיל'] + people_means[k].tolist() + [None, None]
            means_to_print = {frame.columns[i]: tmp[i] for i in range(len(tmp))}
            frame = frame.append(means_to_print, ignore_index=True)

            person_normalized = ['ערך מנורמל לפי סטיות תקן'] + [(people_means[k, i] - means[i]) / stds[i] for i in
                                                                range(13)] + [None, None]
            normalized_to_print = {frame.columns[i]: person_normalized[i] for i in range(len(person_normalized))}
            frame = frame.append(normalized_to_print, ignore_index=True)

            person_grade = ['ציון סופי'] + [str(self.grade(person_normalized[i], i - 1)) for i in range(1, 14)] + [None,
                                                                                                                   None]
            grade_to_print = {frame.columns[i]: person_grade[i] for i in range(len(person_grade))}
            frame = frame.append(grade_to_print, ignore_index=True)

            person_grade = [person] + person_grade[1:]
            grade_to_print = {frame.columns[i]: person_grade[i] for i in range(len(person_grade))}
            people_scores_frame = people_scores_frame.append(grade_to_print, ignore_index=True)
            self.export_to_excel(self._outputs_example_person_path.format(person), frame)

        self.export_to_excel(self._outputs_numeric_summary_path, people_scores_frame)
        print("Finished!")

    def grade(self, normalized_score, question_index):
        res = 0
        if normalized_score < -1.5:
            res = 1
        elif -1.5 <= normalized_score < -0.7:
            res = 2
        elif -0.7 <= normalized_score < 0:
            res = 3
        elif 0 <= normalized_score < 0.7:
            res = 4
        elif 0.7 <= normalized_score < 1.5:
            res = 5
        elif normalized_score >= 1.5:
            res = 6

        if 7 <= question_index <= 12:  # educational questions
            res = (res + 1) // 2

        return res

    def export_to_excel(self, filename, frame):
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        frame.to_excel(writer, sheet_name='גליון1')  # , index=False, header=False)
        workbook = writer.book
        worksheet = writer.sheets['גליון1']
        worksheet.right_to_left()

        # Add a header format.
        header_format = workbook.add_format(
            {'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#BDD7EE', 'border': 1})

        # Write the column headers with the defined format.
        for col_num, value in enumerate(frame.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)

        worksheet.set_column('A:A', 0, None)
        worksheet.set_column('B:B', 11, None)
        worksheet.set_column('C:D', 27.44, None)
        worksheet.set_column('D:D', 23, None)
        worksheet.set_column('E:E', 23, None)
        worksheet.set_column('F:F', 23, None)
        worksheet.set_column('G:G', 23, None)
        worksheet.set_column('H:H', 23, None)
        worksheet.set_column('I:I', 23, None)
        worksheet.set_column('J:J', 18, None)
        worksheet.set_column('K:K', 18, None)
        worksheet.set_column('L:L', 18, None)
        worksheet.set_column('M:M', 18, None)
        worksheet.set_column('N:N', 18, None)
        worksheet.set_column('O:O', 18, None)
        worksheet.set_column('P:P', 45, None)
        worksheet.set_column('Q:Q', 45, None)

        worksheet.set_row(0, 164.4)

        writer.save()
