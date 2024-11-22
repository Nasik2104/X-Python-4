import pandas as pd
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, file_path, chunk_size=100000):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.data = pd.DataFrame()
        self.history = []

    def load_data(self):
        """Load CSV data in chunks for efficient memory usage."""
        chunks = []
        try:
            for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size):
                chunks.append(chunk)
            self.data = pd.concat(chunks, ignore_index=True)
            print(f"Data loaded successfully with {len(self.data)} rows.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def calculate_statistics(self, column):
        """Calculate basic statistics for a given column."""
        if column in self.data.columns:
            avg = self.data[column].mean()
            minimum = self.data[column].min()
            maximum = self.data[column].max()
            return {"avg": avg, "min": minimum, "max": maximum}
        else:
            return None

    def filter_data(self, column, condition, value):
        """Filter data based on a condition (>, <, ==)."""
        if column not in self.data.columns:
            return pd.DataFrame()

        if condition == ">":
            filtered_data = self.data[self.data[column] > value]
        elif condition == "<":
            filtered_data = self.data[self.data[column] < value]
        elif condition == "==":
            filtered_data = self.data[self.data[column] == value]
        else:
            return pd.DataFrame()

        self.history.append({
            "action": "filter",
            "column": column,
            "condition": condition,
            "value": value,
            "result_count": len(filtered_data)
        })
        return filtered_data

    def visualize_data(self, column):
        """Generate a histogram for a specified column."""
        if column in self.data.columns:
            plt.figure(figsize=(10, 6))
            self.data[column].hist(bins=20)
            plt.title(f'Histogram of {column}')
            plt.xlabel(column)
            plt.ylabel('Frequency')
            plt.grid(False)
            plt.show()

    def display_history(self):
        """Display the history of actions performed."""
        if not self.history:
            return "No actions performed yet."
        history_str = ""
        for i, record in enumerate(self.history, start=1):
            history_str += (f"{i}. Action: {record['action']}, Column: {record['column']}, "
                            f"Condition: {record['condition']}, Value: {record['value']}, "
                            f"Result Count: {record['result_count']}\n")
        return history_str

    def get_column_names(self):
        return self.data.columns.tolist()
