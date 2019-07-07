import fnmatch
import os
import time

import matplotlib
import matplotlib.pyplot as plot
import numpy as np
from PyQt5 import QtCore
from mpl_toolkits.basemap import Basemap

import helpers

# Set matplotlib to not use tk while plotting
matplotlib.use('Agg')


class Plotter(QtCore.QThread):
    PLOTS_DIR = "data/plots/"
    NC_FILE_PATH = "data/Complete_TMAX_LatLong1.nc"
    LONGITUDES, LATITUDES, DATES, TEMPERATURES, \
    TEMPERATURE_UNIT = helpers.get_variables_from_nc_file(NC_FILE_PATH)
    image_increment_signal = QtCore.pyqtSignal()
    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, start_date, end_date, step: int, color_map, parent_window=None):
        super(Plotter, self).__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.step = step
        self.stop_plot = False
        self.color_map = plot.get_cmap(color_map)
        self.world_map = Plotter.get_map_format()
        if parent_window is not None:
            parent_window.stop_plot_signal.connect(self.stop)

    def run(self):
        self.start_plotting(self.start_date, self.end_date, self.step)

    def stop(self):
        self.stop_plot = True

    def file_checks(self):
        if not os.path.isfile(self.NC_FILE_NAME):
            self.status_signal.emit(f"{self.NC_FILE_NAME} file not found, exiting")
            return False
        if os.path.isdir(f"/{self.PLOTS_DIR}"):
            self.status_signal.emit(f"{self.PLOTS_DIR} directory not found, exiting")
            return False
        return True

    @staticmethod
    def get_color_maps():
        # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
        color_maps = ["seismic", "coolwarm", "bwr", "gnuplot2", "jet"]
        return color_maps

    @staticmethod
    def get_map_format():
        """
        Source:
            https://matplotlib.org/basemap/api/basemap_api.html
        Returns:
            Basemap: Constructed world basemap
        """
        world_map = Basemap(projection="cyl", llcrnrlat=-90, urcrnrlat=90,
                            llcrnrlon=-180, urcrnrlon=180, resolution="c")
        Plotter.draw_map_details(world_map)
        return world_map

    @staticmethod
    def draw_map_details(world_map):
        world_map.drawcoastlines(linewidth=0.6)
        world_map.drawcountries(linewidth=0.3)

    @staticmethod
    def get_display_date(decimal_date):
        month = decimal_date % 1
        months = {"0.041": "January",
                  "0.125": "February",
                  "0.208": "March",
                  "0.291": "April",
                  "0.375": "May",
                  "0.458": "June",
                  "0.541": "July",
                  "0.625": "August",
                  "0.708": "September",
                  "0.791": "October",
                  "0.875": "November",
                  "0.958": "December"}
        return f"{months[str(month)[:5]]} {int(decimal_date)}"

    @staticmethod
    def clear_plots():
        file_names = os.listdir(Plotter.PLOTS_DIR)
        for file in fnmatch.filter(file_names, "plot*.png"):
            os.remove(os.path.join(Plotter.PLOTS_DIR, file))

    def start_plotting(self, start_date_decimal, end_date_decimal, step):
        start_date_index = helpers.find_nearest_index(Plotter.DATES, start_date_decimal)
        end_date_index = helpers.find_nearest_index(Plotter.DATES, end_date_decimal)
        # end_date_index + 1 to make end_date inclusive
        for count, date_index in enumerate(range(start_date_index, end_date_index + 1, step)):
            if not self.stop_plot:
                self.status_signal.emit(f"Processing image {count + 1}/"
                                        f"{((end_date_index - start_date_index) // step) + 1}")
                start_time = time.time()
                self.create_plot(count, date_index)
                print(f"Took {time.time() - start_time:.2f}s for image {count + 1}")
                self.image_increment_signal.emit()
        self.status_signal.emit("")

    def create_plot(self, count, date_index):
        plot.figure(count)
        color_mesh = self.world_map.pcolormesh(Plotter.LONGITUDES, Plotter.LATITUDES,
                                               np.squeeze(Plotter.TEMPERATURES[date_index]),
                                               cmap=self.color_map)
        color_bar = self.world_map.colorbar(color_mesh, location="bottom", pad="10%")
        color_bar.set_label(Plotter.TEMPERATURE_UNIT)
        Plotter.draw_map_details(self.world_map)
        date = Plotter.get_display_date(Plotter.DATES[date_index])
        plot.title(f"Plot for {date}")
        # This scales the plot to -10,10 making those 2 mark "extremes"
        # but if we have a change bigger than 10
        # we won't be able to see it other than
        # it being extra red (aka we won't know if it's +11 or +15)
        plot.clim(-10, 10)
        file_path = f"{Plotter.PLOTS_DIR}plot{count}.png"
        # bbox_inches="tight" remove whitespace around the image
        # facecolor=(0.94, 0.94, 0.94) , background color of image
        plot.savefig(file_path, dpi=142, bbox_inches="tight", facecolor=(0.94, 0.94, 0.94))
        plot.close()

    def create_graph(self):
        """
            Creates graph with data from TEMPERATURES from range start_date to end_date
            Output is saved as graph.png
            Works with step value, example step of 12 will only plot values for each year.
            Note that end_date doesn't necessarily has to be plotted, for example if step
            is 12 and start_date = 1998.125 , end_date = 2000.7083333333333 the last plotted
            date will be 2000.125
        """

        # We need to slice the arrays so it only has values from start_date to end_date
        dates_start_index = helpers.find_nearest_index(Plotter.DATES, self.start_date)
        # +1 to make the end_date included
        dates_end_index = helpers.find_nearest_index(Plotter.DATES, self.end_date) + 1

        # Slice the TEMPERATURES array so that values only fall in start_date to end_date range
        # Remember that the format of TEMPERATURE array is [[time][latitude][longitude]]
        sliced_temperatures = Plotter.TEMPERATURES[dates_start_index:dates_end_index]

        # Find the mean value of temperature anomaly for each step in sliced_temperatures
        # Exclude nan values - those are just areas with no measurements, like parts of oceans
        # and in older dates part of land masses without weather stations.
        # We don't necessarily calculate the mean for each date, depending on the step value.
        # If, for example, step is 3 then each third temperature sublist will be calculated.
        temperature_means_to_plot = [np.nanmean(sliced_temperatures[i]) for i in
                                     range(0, len(sliced_temperatures), self.step)]

        # Slice the DATES array so that values only fall in start_date to end_date range
        sliced_dates = Plotter.DATES[dates_start_index:dates_end_index]

        # Depending on step, not all dates from sliced_dates will be plotted, example for
        # step 3 each third date will be plotted.
        dates_to_plot = [sliced_dates[i] for i in range(0, len(sliced_dates), self.step)]

        # Set plot size for the plot
        plot.rcParams["figure.figsize"] = (8, 8)

        # Create the plot space upon which to plot the data
        fig, ax = plot.subplots()

        # Add the x-axis and the y-axis to the plot
        ax.plot(dates_to_plot, temperature_means_to_plot, color="red", linewidth=0.5)
        ax.set(xlabel="Month", ylabel="Average Air Surface Temperature Anomaly (C)")

        # Save the plot to image file
        file_path = f"{Plotter.PLOTS_DIR}graph.png"
        plot.savefig(file_path, dpi=142, bbox_inches="tight", facecolor=(0.94, 0.94, 0.94))
        plot.close()


if __name__ == "__main__":
    p = Plotter(1994.125, 2000.7083333333333, 1, "seismic")
    p.start()
    while not p.isFinished():
        time.sleep(10)
