import matplotlib.pyplot as plt
import sys

sys.path.insert(0, '../..')


class Visualization:
    def __init__(self):
        self.trajectory = plt.figure(1)
        self.error = plt.figure(2)

    @staticmethod
    def plot_trajectory(x=None, y=None, x_est=None, y_est=None, x_gps=None, y_gps=None, sav_fig=False):
        """
        Plot trajectory
        x: True trajectory x
        y: True trajectory y
        x_est: Estimated trajectory x
        y_est: Estimated trajectory y
        x_gps: True trajectory x
        y_gps: True trajectory x
        """
        plt.figure(1)
        if x and y:
            plt.plot(x, y, color='blue', marker='x', linestyle='solid', linewidth=2, markersize=6,
                     label="Odom Trajectory")

        if x_gps and y_gps:
            plt.plot(x_gps, y_gps, color='blue', linestyle='solid', marker='x', markersize=6, label="GPS Trajectory")

        if x_est and y_est:
            plt.plot(x_est, y_est, 'ro', linestyle='dashed', linewidth=2, markersize=4, label="Estimated Trajectory")

        plt.xlabel('X (m)', fontsize=18)
        plt.ylabel('Y (m)', fontsize=18)
        plt.legend(loc='upper right')
        plt.title('Linear Kalman Filter')
        if sav_fig:
            plt.savefig('plots/using_all_sensors.png', dpi=300)

    @staticmethod
    def plot_error(x, y, save_fig=False):
        """
        Plot error curve
        x: time
        y: root mean square error
        """
        plt.figure(2)
        plt.plot(x, y)
        plt.xlabel('Time (s)', fontsize=18)
        plt.ylabel('RMSE (m)', fontsize=18)
        plt.title('Position error in meters')
        if save_fig:
            plt.savefig('plots/gps_error.png')
        plt.show()
