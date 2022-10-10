import pandas as pd
import numpy as np


class Odometry:

    def __init__(self):
        # Read data file
        self._data_file = pd.read_csv('data/odometry.csv')
        # initialise variables
        self.timestamp_secs = None
        self.timestamp_nsecs = None
        self.pose = []
        self.pose_covariance = []
        self.twist = []
        self.twist_covariance = []
        self._index = 0
        # Initialise all the values
        self.update_data()

    def update_data(self):
        """
        Update values when called return True if update successful or false
        """
        self.timestamp_secs = self._data_file.iloc[self._index, 0]
        self.timestamp_nsecs = self._data_file.iloc[self._index, 1]
        self.pose = self._data_file.iloc[self._index, 2:9].values
        self.pose_covariance = np.reshape(list(map(float, self._data_file.iloc[self._index, 9][1:-1].split(','))),
                                          (6, 6))
        self.twist = self._data_file.iloc[self._index, 10:16].values
        self.twist_covariance = np.reshape(list(map(float, self._data_file.iloc[self._index, 16][1:-1].split(','))),
                                           (6, 6))

        # if end of the file is not reached return True saying sensor reading is valid
        if self._index != self._data_file.shape[0]-1:
            self._index += 1
            return True

        return False

