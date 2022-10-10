import pandas as pd
import numpy as np
import pyproj
import scipy
from scripts.Transform import Transform


class GPS(Transform):

    def __init__(self):
        # Get the transformations from calib.yaml
        super().__init__()

        # read data file
        self._gps_data = pd.read_csv("data/gps.csv")

        # initialise variables
        self.timestamp_secs = None
        self.timestamp_nsecs = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.covariance = None
        self._index = 0

        # initialise values
        self.update_data()

    def update_data(self):
        """
        Update values when called return false if reached end of file
        """
        self.timestamp_secs = self._gps_data.iloc[self._index, 0]
        self.timestamp_nsecs = self._gps_data.iloc[self._index, 1]
        # convert lat lon alti to x,y,z in base coordinate frame
        transformed_pos = self._transform()
        self.latitude = transformed_pos[0]
        self.longitude = transformed_pos[1]
        self.altitude = transformed_pos[2]
        self.covariance = np.reshape(self._gps_data.iloc[self._index, 5:14].values, (3, 3))

        # if end of file is not reached update index
        if self._index != self._gps_data.shape[0] - 1:
            self._index += 1
            return True

        # sensor fails
        return False

    def _transform(self):
        # convert to local ENU system with 1st values of lat lon alti as origin
        pos = self._geodetic2enu(self._gps_data.iloc[self._index, 2],
                                 self._gps_data.iloc[self._index, 3],
                                 self._gps_data.iloc[self._index, 4],
                                 self._gps_data.iloc[0, 2],
                                 self._gps_data.iloc[0, 3],
                                 self._gps_data.iloc[0, 4])
        # Transform to base coordinate frame using transformations provided in calib.yaml
        pos = np.concatenate((pos, [1]), axis=0)
        transformed_pos = self.gps_to_baselink.dot(pos)
        return transformed_pos

    @staticmethod
    def _geodetic2enu(lat, lon, alt, lat_org, lon_org, alt_org):
        """
        param lat: latitude
        param lon: longitude
        param alt: altitude
        param lat_org: origin latitude
        param lon_org: origin longitude
        param alt_org: origin longitude
        return: x,y,z position in ENU coordinate frame
        """
        transformer = pyproj.Transformer.from_crs(
            {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
            {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
        )
        x, y, z = transformer.transform(lon, lat, alt, radians=False)
        x_org, y_org, z_org = transformer.transform(lon_org, lat_org, alt_org, radians=False)
        vec = np.array([[x - x_org, y - y_org, z - z_org]]).T

        rot1 = scipy.spatial.transform.Rotation.from_euler('x', -(90 - lat_org),
                                                           degrees=True).as_matrix()  # angle*-1 : left handed *-1
        rot3 = scipy.spatial.transform.Rotation.from_euler('z', -(90 + lon_org),
                                                           degrees=True).as_matrix()  # angle*-1 : left handed *-1

        rot_matrix = rot1.dot(rot3)

        enu = rot_matrix.dot(vec).T.ravel()
        return enu.T
