import pandas as pd


def load_and_print_df(csv_path: str):
		
		# TODO: Read csv from csv_path
		
		csv_path = csv_path
		useful_columns = ['LocationDesc', 'Question', 'Data_Value', 'StratificationCategory1', 'Stratification1']
		with open(csv_path, 'r') as csv_file:
			df = pd.read_csv(csv_file, usecols = useful_columns)

		df.to_csv("formatted_data.csv", index=True, columns=useful_columns)

		# # Or for a more text-like display similar to what you see in VS Code:
		# with open("a.txt", "w") as f:
		# 	f.write(df.to_string())


# Example usage
if __name__ == "__main__":
    # Replace with your actual CSV path
    csv_file_path = "../nutrition_activity_obesity_usa_subset.csv"
    dataframe = load_and_print_df(csv_file_path)
	sorted_state_means = get_state_means()