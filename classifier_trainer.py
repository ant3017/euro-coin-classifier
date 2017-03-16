import numpy as np
import cv2
import os
import pandas


class Coin:
    """Coin class for a euro coin."""

    def __init__(self, bgr):
        """Initializes the euro coin object."""
        self.bgr = bgr
        self.gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        self.hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        width, height, depth = img.shape
        self.r = width / 2
        self.__process_color()

    def __process_color(self):
        """Process the colors of this coin's center area."""
        # Only use half of the coin area to determine it's center color
        r = self.r * 0.5

        roi = self.hsv[int(self.r-r):int(self.r+r), int(self.r-r):int(self.r+r)]

        if len(roi) > 0:
            self.hue = (sum([pixel[0] for rows in roi for pixel in rows])
                / len(roi) / len(roi[0]))
            self.saturation = (sum([pixel[1] for rows in roi for pixel in rows])
                / len(roi) / len(roi[0]))
            self.lightness = (sum([pixel[2] for rows in roi for pixel in rows])
                / len(roi) / len(roi[0]))


class ContinuousFeature:
    """This class helps to analyze a continous feature"""

    columns = ['Count', 'Min', '1st Quart', 'Mean', 'Median', '3rd Quart',
        'Max', 'Std Dev']

    def __init__(self, data):
        self.count = len(data)
        self.minimum = (min(data))
        self.maximum = (max(data))
        self.mean = (sum(data) / float(len(data)))
        self.f_quartile = (np.percentile(data, 25))
        self.t_quartile = (np.percentile(data, 75))
        self.median = (np.median(np.array(data)))
        self.std_deviation = (np.std(data))

    def get_results(self):
        return [self.count, self.minimum, self.f_quartile, self.mean,
            self.median, self.t_quartile, self.maximum, self.std_deviation]


if __name__ == "__main__":
    # If this script is running as a standalone program

    denominations = ['5c', '10c', '20c', '50c', '1e', '2e']

    for d in denominations:

        print('Processing "' + d + '" denomination...')

        coins = []

        for root, dirs, files in os.walk('data/' + d):
            for f in files:
                if root.startswith('data/.git'):
                    continue
                file_name = os.path.join(root, f)
                #print('Processing ' + file_name + '...')
                img = cv2.imread(file_name)
                coin = Coin(img)
                coins.append(coin)

        hue = ContinuousFeature([c.hue for c in coins])
        saturation = ContinuousFeature([c.saturation for c in coins])
        lightness = ContinuousFeature([c.lightness for c in coins])
        df = pandas.DataFrame([hue.get_results(), saturation.get_results(),
            lightness.get_results()], index=['Hue', 'Saturation', 'Lightness'])
        df.columns = ContinuousFeature.columns
        df.to_csv('./reports/' + d + '.csv')
