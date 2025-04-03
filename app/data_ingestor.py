"""
    This module handles data ingestion and analysis for health statistics.
"""

import pandas as pd

class DataIngestor:

    """
        It loads the data from the csv file.
        It computes different results regarding nutrition, activity, and obesity rate.
    """

    def __init__(self, csv_path: str):

        """
            It reads the data from the csv file, using only the necessary columns.
            It stores the result in a two-dimensional data structure from pandas DataFrame.
        """

        self.csv_path = csv_path
        self.useful_columns = ['LocationDesc', 'Question', 'Data_Value',
                               'Stratification1', 'StratificationCategory1']
        with open(self.csv_path, 'r', encoding = 'utf-8') as csv_file:
            self.df = pd.read_csv(csv_file, usecols = self.useful_columns)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            ('Percent of adults who achieve at least 150 minutes a week of '
              'moderate-intensity aerobic physical activity or 75 minutes a '
              'week of vigorous-intensity aerobic activity (or an equivalent combination)'),

            ('Percent of adults who achieve at least 150 minutes a week of '
             'moderate-intensity aerobic physical activity or 75 minutes a '
             ' week of vigorous-intensity aerobic physical activity and engage '
             ' in muscle-strengthening activities on 2 or more days a week'),

            ('Percent of adults who achieve at least 300 minutes a week of '
             'moderate-intensity aerobic physical activity or 150 minutes a '
             'week of vigorous-intensity aerobic activity (or an equivalent combination)'),

            ('Percent of adults who engage in muscle-strengthening activities '
             'on 2 or more days a week'),
        ]

    def get_states_mean(self, question):

        """
            It takes a question and calculates the average values for each state, 
            then sorts the results in ascending order.
        """

        question_matches = self.df['Question'] == question
        question_data = self.df[question_matches]

        grouped_by_state = question_data.groupby('LocationDesc')
        sorted_state_means = grouped_by_state['Data_Value'].mean().sort_values(ascending = True)

        return sorted_state_means.to_dict()


    def get_state_mean(self, state, question):

        """
            It takes a specific question and a state, then calculates the
            average recorded value for that state.
        """

        question_matches = self.df['Question'] == question
        question_data = self.df[question_matches]

        state_matches = question_data['LocationDesc'] == state
        filtered_data = question_data[state_matches]

        state_mean = filtered_data['Data_Value'].mean()

        return {state: float(state_mean)}


    def get_best5(self, question):

        """
            It takes a question and calculates the average recorded values for all 
            states, then returns the top 5 states based on those averages.
        """

        sorted_state_means = self.get_states_mean(question)

        values = list(sorted_state_means.items())

        best5 = {}

        if question in self.questions_best_is_min:
            best5 = dict(values[:5])
        else:
            best5 = dict(values[::-1][:5])   #  reverse and take the first elements

        return best5


    def get_worst5(self, question):

        """
            It takes a question and calculates the average recorded values for all 
            states, then returns the bottom 5 states based on those averages.
        """

        sorted_state_means = self.get_states_mean(question)

        values = list(sorted_state_means.items())

        worst5 = {}

        if question in self.questions_best_is_min:
            worst5 = dict(values[::-1][:5])
        else:
            worst5 = dict(values[:5])

        return worst5


    def get_global_mean(self, question):

        """
            It takes a question and calculates the overall average of recorded values
            from the entire dataset.
        """

        question_matches = self.df['Question'] == question
        question_data = self.df[question_matches]

        global_mean = question_data['Data_Value'].mean()

        return {"global_mean": float(global_mean)}


    def get_diff_from_mean(self, question):

        """
            It takes a question and calculates the difference between the global 
            average and each state's average for all states in the dataset.
        """

        global_mean = self.get_global_mean(question)
        sorted_state_means = self.get_states_mean(question)

        diff_from_mean = {}

        for state, mean in sorted_state_means.items():
            diff_from_mean[state] = global_mean["global_mean"] - mean

        return diff_from_mean


    def get_state_diff_from_mean(self, state, question):

        """
            It takes a question and a specific state, then calculates the difference
            between the global average and that particular state's average.
        """

        global_mean = self.get_global_mean(question)
        state_mean = self.get_state_mean(state, question)

        return {state: float(global_mean["global_mean"] - state_mean[state])}


    def get_mean_by_category(self, question):

        """
            It takes a question and calculates the average value for each segment 
            (Stratification1) within each category (StratificationCategory1) for every state.
        """

        question_matches = self.df['Question'] == question
        question_data = self.df[question_matches]

        result = {}

        grouped = question_data.groupby(['LocationDesc', 'StratificationCategory1',
                                         'Stratification1'])

        for (state, category, segment), group_data in grouped:
            key = f"('{state}', '{category}', '{segment}')"
            result[key] = group_data['Data_Value'].mean()

        return result


    def get_state_mean_by_category(self, state, question):

        """
            It takes a question and a specific state, then calculates the 
            average value for each segment (Stratification1) within each category
            (StratificationCategory1) for that particular state.
        """

        question_matches = self.df['Question'] == question
        question_data = self.df[question_matches]

        state_matches = question_data['LocationDesc'] == state
        filtered_data = question_data[state_matches]

        result = {state: {}}

        grouped_by_category_segment = filtered_data.groupby(['StratificationCategory1',
                                                             'Stratification1'])

        for (category, segment), group_data in grouped_by_category_segment:
            key = f"('{category}', '{segment}')"
            result[state][key] = group_data['Data_Value'].mean()

        return result
