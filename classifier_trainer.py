#! /usr/bin/python
CLASSIFIER_COMMENT = """
    Euro Coin Detector Classifier
    Created by Chen Yumin (http://chenyumin.com)
////////////////////////////////////////////////////////////////////////////////
 This software is provided by the copyright holders and contributors 'as is' and
 any express or implied warranties, including, but not limited to, the implied
 warranties of merchantability and fitness for a particular purpose are disclaimed.
 In no event shall the Intel Corporation or contributors be liable for any direct,
 indirect, incidental, special, exemplary, or consequential damages
 (including, but not limited to, procurement of substitute goods or services;
 loss of use, data, or profits; or business interruption) however caused
 and on any theory of liability, whether in contract, strict liability,
 or tort (including negligence or otherwise) arising in any way out of
 the use of this software, even if advised of the possibility of such damage.
////////////////////////////////////////////////////////////////////////////////
"""

import numpy as np
import cv2
import os
import pandas
import json
import csv


class Coin:
    """Coin class for a euro coin."""

    def __init__(self, src):
        """Initializes the euro coin object."""

        # If source is a dictionary, creating from cache
        if isinstance(src, dict):
            self.hue = int(src['hue'])
            self.saturation = int(src['saturation'])
            self.lightness = int(src['lightness'])
            return

        # Else source is a bgr stream image
        bgr = src

        # Convert to YUV color space
        self.yuv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV)
        # Contrast stretching, equalize the histogram of the Y channel
        self.yuv[:,:,0] = cv2.equalizeHist(self.yuv[:,:,0])
        # convert the YUV image back to RGB format
        self.bgr = cv2.cvtColor(self.yuv, cv2.COLOR_YUV2BGR)
        self.gray = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2GRAY)
        self.hsv = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2HSV)
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
        self.hist, bin_edges = np.histogram(data, bins=range(256))
        self.hist = self.hist.tolist()

    def to_list(self):
        return [self.count, self.minimum, self.f_quartile, self.mean,
            self.median, self.t_quartile, self.maximum, self.std_deviation]

    def to_dict(self):
        d = {}
        d.update(vars(self))
        return d


if __name__ == "__main__":
    # If this script is running as a standalone program

    classifier = {
        '__comment': CLASSIFIER_COMMENT.split("\n"),
        'author': 'Chen Yumin',
        'website': 'http://chenyumin.com',
        'name': 'Euro Coin Detector Classifier',
        'version': '1.0.0',
        'classification': {}
    }

    denominations = {'1c':'Xc/1c', '2c':'Xc/2c', '5c':'Xc/5c', 'Xc':'Xc',
        '10c':'X0c/10c', '20c':'X0c/20c', '50c':'X0c/50c', 'X0c':'X0c',
        '1e':'1e', '2e':'2e'}


    for d in denominations:

        print('Processing "' + d + '" denomination...')

        coins = {}
        new_count = 0
        cache_count = 0
        cache_read_count = 0

        # If cache file exists, read from cache
        try:
            with open('cache/' + d + '.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    coins[row['filename']] = Coin(row)
                    cache_read_count += 1
        except:
            pass

        # Cache processed data
        with open('cache/' + d + '.csv', 'w') as csvfile:
            fieldnames = ['filename', 'hue', 'saturation', 'lightness']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for root, dirs, files in os.walk('data/' + denominations[d]):
                for f in files:
                    if root.startswith('data/.git'):
                        # Skip .git folder
                        continue
                    if f in coins:
                        # Skip cached data
                        cache_count += 1
                        continue

                    file_name = os.path.join(root, f)
                    #print('Processing ' + file_name + '...')
                    img = cv2.imread(file_name)
                    coins[f] = Coin(img)

                    # Write this coin to cache
                    writer.writerow({
                        'filename': f,
                        'hue': coins[f].hue,
                        'saturation': coins[f].saturation,
                        'lightness': coins[f].lightness
                    })

                    new_count += 1

        if cache_count != cache_read_count:
            print "Error: Cache count doesn't match."

        print("Gathered " + str(cache_count + new_count) + " items, " +
            str(cache_count) + " of which are from cache.")
            
        hue = ContinuousFeature([c.hue for c in coins.itervalues()])
        saturation = ContinuousFeature([c.saturation for c in coins.itervalues()])
        lightness = ContinuousFeature([c.lightness for c in coins.itervalues()])

        result = [hue, saturation, lightness]

        classifier['classification'][d] = {'hue': hue.to_dict(), 'saturation':
            saturation.to_dict(), 'lightness': lightness.to_dict()}

        # Generate Reports
        df = pandas.DataFrame([hue.to_list(), saturation.to_list(),
            lightness.to_list()], index=['Hue', 'Saturation', 'Lightness'])
        df.columns = ContinuousFeature.columns
        df.to_csv('./reports/' + d + '.csv')

    with open('euro_coin_detector_classifier.json', 'w') as fp:
        json.dump(classifier, fp, indent=4, separators=(',', ': '),
            sort_keys=False)
