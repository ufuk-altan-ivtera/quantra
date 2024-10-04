from ...mark.signal import Sequentialize

class CreateSequencePipeline(Sequentialize):
    
    def __init__(self, throwback_period, training_columns):
        
        self.throwback_period = throwback_period
        self.training_columns = training_columns
        
    def create_sequence_label(self, value):

        if value >= 65:
            label = 'm'
        elif value <= 40:
            label = 'w'
        else:
            label = 's'

        return label

    def create_column_names(self):

        column_names = []
        for column in self.training_columns:
            for i in  range(1, self.throwback_period + 2):
                column_names.append(column + str(i))
        return column_names

    def create_flattened_values_lol(self, filtered_df, df):

        flattened_values_lol = []

        for index in filtered_df['Index']:

            throwback_index = index - self.throwback_period

            if throwback_index > 0:
                subdf = df[(df['Index'] >= throwback_index) & (df['Index'] <= index)]

                flattened_values = self.sequentialize_flattened_values(subdf, self.training_columns)

                label = subdf['Label'][-1]
                flattened_values.append(label)

                flattened_values_lol.append(flattened_values)

            else:
                pass

        return flattened_values_lol
