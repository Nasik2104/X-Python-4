import pandas as pd
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, file_path, chunk_size=100000):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.data = pd.DataFrame()

    def load_data(self):
        chunks = []
        try:
            for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size):
                chunks.append(chunk)
            self.data = pd.concat(chunks, ignore_index=True)
            print(f"Data loaded successfully with {len(self.data)} rows.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def calculate_statistics(self, column):
        if column in self.data.columns:
            avg = self.data[column].mean()
            minimum = self.data[column].min()
            maximum = self.data[column].max()
            return {"avg": avg, "min": minimum, "max": maximum}
        else:
            return None

    def filter_data(self, column, condition, value):
        if column not in self.data.columns:
            return pd.DataFrame()

        if condition == ">":
            self.data = self.data[self.data[column] > value]
        elif condition == "<":
            self.data = self.data[self.data[column] < value]
        elif condition == "==":
            self.data = self.data[self.data[column] == value]
        else:
            return pd.DataFrame()

        print(f"Data after filter {len(self.data)}")
