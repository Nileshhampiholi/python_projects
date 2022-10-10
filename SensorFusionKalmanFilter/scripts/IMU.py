import pandas as pd
import numpy as np
from scripts.Transform import Transform


class IMU(Transform):

    def __init__(self):
        # get transformation from calib.yaml
        super().__init__()

        # read data file
        self._data_file = pd.read_csv('data/imu.csv')

        # initialise variables
        self.timestamp_secs = None
        self.timestamp_nsecs = None

        self.orientation = []
        self.orientation_covariance = []

        self.angular_velocity = []
        self.angular_velocity_covariance = []

        self.linear_velocity = []
        self.linear_velocity_covariance = []

        self._index = 0

        # initialise values
        self.update_data()

    def update_data(self):
        """
        Update values when called return false if reached end of file
        """
        self.timestamp_secs = self._data_file.iloc[self._index, 0]
        self.timestamp_nsecs = self._data_file.iloc[self._index, 1]

        self.orientation = self._data_file.iloc[self._index, 2:6].values
        self.orientation_covariance = np.reshape(self._data_file.iloc[self._index, 6:15].values, (3, 3))

        self.angular_velocity = self._data_file.iloc[self._index, 15:18].values
        self.angular_velocity_covariance = np.reshape(self._data_file.iloc[self._index, 18:27].values, (3, 3))

        # Transform to base coordinate frame using transformations provided in calib.yaml
        self.linear_velocity = self._transform()
        self.linear_velocity_covariance = np.reshape(self._data_file.iloc[self._index, 30:39].values, (3, 3))

        # if end of file is not reached update index
        if self._index != self._data_file.shape[0]-1:
            self._index += 1
            return True

        return False

    def _transform(self):
        # Transform to base coordinate frame using transformations provided in calib.yaml
        lin_acc = self._data_file.iloc[self._index, 27:30].values + self.imu_acc_offset
        transformed = self.imu_to_baselink[0:3, 0:3].dot(lin_acc)
        return transformed
