import pandas as pd


class Dfprep:
    def __init__(self, name):
        self.name = name
        self.filename = None
        self.raw_data = None
        self.one_hot_data = None
        self.clean_data = None
        self.measurable_columns = None

    def load_data(self, filename, **kwargs):
        # self.filename = filename
        self.raw_data = pd.read_csv(filename, **kwargs)
        # self.raw_data = pd.read_csv(self.filename, **kwargs)

    # def view_raw_data(self):
    #     print('')

    def remove_columns(self, columns, **kwargs):
        self.raw_data.drop(columns, axis=1, inplace=True, **kwargs)

    def remove_lines(self, lines, **kwargs):
        self.raw_data.drop(lines, axis=0, inplace=True, **kwargs)

    def rename_columns(self, old_names, new_names):
        pass

    def convert_categories(self, categories):
        categorical = pd.get_dummies(self.raw_data[categories])
        self.one_hot_data = pd.concat([self.raw_data, categorical], axis=1, sort=False)

    def _detect_measurable_columns(self):
        self.measurable_columns = [col for col in self.raw_data.columns if type(col) == int]

    def prepare_for_euklid(self, line):
        self._detect_measurable_columns()
        return self.one_hot_data.loc[line, self.measurable_columns].values.astype('int')
