import yaml
import numpy as np
from scipy.spatial.transform import Rotation as R
import sys

sys.path.insert(0, '../..')


class Transform:
    def __init__(self):
        # Read file

        with open("resources/calib.yaml", "r") as stream:
            try:
                self._transforms = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        # Get all transformations
        self.gps_to_baselink = self._get_gps_to_baselink()
        self.odom_to_baselink = self._get_odom_to_baselink()
        self.imu_to_baselink = self._get_imu_to_baselink()
        self.imu_acc_offset = self._transforms['imu']['acc_offset']
        self.imu_gyro_offset = self._transforms['imu']['gyro_offset']

    def _get_gps_to_baselink(self):
        """
        Get transformation from gps to baselink
        """
        tf = np.zeros((4, 4), dtype=np.float64)
        pos = self._transforms['gps']['position_gps_baselink']
        orientation = self._transforms['gps']['orientation_gps_baselink']
        orientation = R.from_quat(orientation)

        tf[0:3, 0:3] = orientation.as_matrix()
        tf[0:3, 3] = pos

        return tf

    def _get_odom_to_baselink(self):
        """
           Get transformation from odom to baselink
           It is same coordinate system so ignored
        """
        tf = np.identity(4, dtype=np.float64)
        pos = self._transforms['odom']['position_baselink_odom']
        # orientation = self._transforms['odom']['rotation_euler']
        # orientation = R.from_euler('zyx', orientation, degrees=True)

        # tf[0:3, 0:3] = orientation.as_matrix()
        # tf[0:3, 3] = pos
        # tf = np.linalg.inv(tf)

        return tf

    def _get_imu_to_baselink(self):
        """
           Get transformation from imu to baselink
        """
        tf = np.zeros((4, 4), dtype=np.float64)
        pos = self._transforms['imu']['position_imu_baselink']
        orientation = self._transforms['imu']['rotation_imu_baselink']
        orientation = R.from_quat(orientation)

        tf[0:3, 0:3] = orientation.as_matrix()
        tf[0:3, 3] = pos

        return tf
