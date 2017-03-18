**Euro Coin Classifier**
========================
<sup>*This Euro Coin Classifier is part of the [Euro Coin Detector][4] project.*</sup>  
<sup>*The Main GitHub Repository: [Euro Coin Detector](https://github.com/chen-yumin/euro-coin-detector)*</sup>  


Introduction
------------------------
This **Euro Coin Classifier** is part of the [Euro Coin Detector][4] project that aims to locate and recognize euro coins from natural images and classify them according to their coin denomination and tell their values.

The training of this classifier uses statistics and data mining techniques to extract and process information from many images of the euro coin series of each denomination. The goal is to predict and generalize each euro coin type's attributes using *Machine Learning for Predictive Data Analytics* techniques.

The classifier is developed using *Artificial Intelligence* to describe the euro coins' shape, size, color, patterns, etc. so later the classifier can be used to determine whether an arbitrary object is a certain denomination of euro coin.  


Data Exploration and Analytics
------------------------
The reports are focused on *Descriptive Statistics* analytics. For each euro coin denomination, its HSI (Hue, Saturation, Intensity) and LUV (Luma, Blue Difference, Red Difference) color space values are the main area of interests.  

The reports can be found under the [reports](reports) folder.  


Data Preparation
------------------------
The [dataset_collector.py](dataset_collector.py) script is used to prepare dataset for the training of the classifier. It uses computer vision techniques to recognize and segment euro coins from natural images, and output the segmented coins into the *output* folder.  

The dataset collector takes natural images of euro coins as input, and process them into segmented image dataset that is ready for the classifier training process.  

Usage:

    python dataset_collector.py [image_files...]  

Multiple image files can be all passed at once to batch process them all.

Example:  

| Original | Processed |
| :---: | :---: |
| ![Original](doc/img/dataset-collector-before.jpg) | ![Processed](doc/img/dataset-collector-after.jpg) |
  
Original: A natural image of 22 euro coins scattered on a surface.  
Processed: 22 separate images of euro coins cropped to just the coins themselves.  



Licensing
------------------------
Please see the file named [LICENSE.md](LICENSE.md).


Author
------------------------
* Chen Yumin  


Contact
------------------------
* Chen Yumin: [*http://chenyumin.com/*][1]
* CharmySoft: [*http://CharmySoft.com/*][2]  
* About: [*http://CharmySoft.com/about*][3]  
* Email: [*hello@chenyumin.com*](mailto:hello@chenyumin.com)  

[1]: http://chenyumin.com/ "Chen Yumin"
[2]: http://www.CharmySoft.com/ "CharmySoft"
[3]: http://www.CharmySoft.com/about "About CharmySoft"
[4]: http://www.CharmySoft.com/app/euro-coin-detector "Euro Coin Detector"