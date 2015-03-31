


## 2012-01-07 ##

### General ###
  1. All files in processing/plots have been reprocessed with julendat revision f68e6fb4cc7d. See **warning** reason 1.
  1. A backup file has been created afterwards: `ki_processing_plots_2011-01-07_182243.7z`
  1. Afterwards, files from `processing_local_201111241518.zip` have been extracted and moved into the actual processing folder using copy/paste function from dolphin. The number of files has been checked so it seems that everything worked fine.
  1. Files from `processing_local_201111241518.zip` have been processed with julendat revision f68e6fb4cc7d. See **warning** reason 2.
  1. A backup file has been created afterwards: `ki_processing_plots_2011-01-07_193946.7z`

The actual working copy can be found on data server 003.

### Warning ###

The following files have not been processed due to two different reasons.

Reason 1: The plot name as indicated in the file name does not match the plot name in the actual inventory file. This could be due to changes of the inventory file after the initial file processing with the GUI-Tool. Only those files are affected which have already been processed in autumn 2011. The naming of the files follows the form: `<plot1>-or-<plot2>` where `<plot1>` is the plot extracted from the file name and `<plot2>` the one from the inventory
```
ki/0000gra0/ra01_nas02_0000/ki_0000gra0_000rug_201012200000_201012210318_mez_ra01_nas02_0000.asc.gra0-or-gra1
ki/0000mai1/ra01_nai05_0000/ki_0000mai1_000pu1_201104152200_201109150820_mez_ra01_nai05_0000.asc.mai1-or-mai0
ki/0000mai1/ra01_nai05_0000/ki_0000mai1_000wxt_201104152200_201107182200_mez_ra01_nai05_0000.asc.mai1-or-mai0
ki/0000mai1/ra01_nai05_0000/ki_0000mai1_000wxt_201104152200_201109150730_mez_ra01_nai05_0000.asc.mai1-or-mai0
ki/0000nkw1/ra01_nai01_0000/ki_0000nkw1_000pu1_201103241030_201103271144_mez_ra01_nai01_0000.asc.nkw1-or-cof3
ki/0000nkw1/ra01_nai01_0000/ki_0000nkw1_000pu1_201103200900_201103240810_mez_ra01_nai01_0000.asc.nkw1-or-cof3
ki/0000sav4/ra01_nai05_0000/ki_0000sav4_000wxt_201104072200_201104131225_mez_ra01_nai05_0000.asc.sav4-or-sav0
ki/0000sav4/ra01_nai05_0000/ki_0000sav4_000wxt_201104072200_201104180950_mez_ra01_nai05_0000.asc.sav4-or-sav0
ki/0000sav4/ra01_nai05_0000/ki_0000sav4_000wxt_201104072200_201108242315_mez_ra01_nai05_0000.asc.sav4-or-sav0
```


Reason 2: The logger serial number is not in the inventory. Only those files are affected which have been extracted from the `processing_local_201111241518.zip` file (see above). Maybe the files have been renamed manually or a different inventory file has been used.
```
ki/0000sav2/ra01_nai05_0000/ki_0000sav2_000rug_201110130900_201111101035_mez_ra01_nai05_0000.asc.not-in-inventory
ki/0000sav4/ra01_nai05_0000/ki_0000sav4_000pu1_201110180810_201111161205_mez_ra01_nai05_0000.asc.not-in-inventory
```



## 2012-01-09 ##
### General ###
  1. All files in processing/plots have been reprocessed with julendat revision 5f4ba78e43e5 because of a bug in the level 0050 processing leading to level 0050 files which only encompass the last level 0005 contents of the respective month.
  1. Files from warning from 2012-01-07 have not been processed.


## 2012-01-10 ##

### General ###
  1. Rename already processed fod2 files to fod1 (processed on 201201091324) according to the kidia protocol from 05.12.2012.
  1. Adjust the station inventory file (fod2 to fod1)
  1. Rename the following files from mai1 to mai0 (station inventory has already been updated) because the plot names have changed (i. e. nor error in the processing chains) - the same has been done for the corresponding rb01 files:
```
ki_0000mai0_000wxt_201104152200_201107182200_mez_ra01_nai05_0000.asc
ki_0000mai0_000wxt_201104152200_201109150730_mez_ra01_nai05_0000.asc
ki_0000mai0_000pu1_201104152200_201109150820_mez_ra01_nai05_0000.asc
```
  1. Add rug logger on sav2 to inventory (51021020183 until 2011-12-27 and 51021020188 starting on 2011-12-27). Ephraihm has replaced the logger because of a mail function in the 51021020183 model.
  1. Rename pu1 (80081025283) from cof3 to nkw1 for the time period until 2011-03-27 and adjust station inventory.
  1. Rename the following files from sav4 to sav0 and add pu1 (80081025288) to station inventory (wxts are already in station inventory) because the plot names have changed (i. e. nor error in the processing chains) - the same has been done for the corresponding rb01 files:
```
ki_0000sav0_000wxt_201104072200_201104131225_mez_ra01_nai05_0000.asc
ki_0000sav0_000wxt_201104072200_201104180950_mez_ra01_nai05_0000.asc
ki_0000sav0_000wxt_201104072200_201108242315_mez_ra01_nai05_0000.asc
ki_0000sav0_000pu1_201110180810_201111161205_mez_ra01_nai05_0000.asc
```
  1. Add new pu1 rain gauge on sav0 (80081025288) to station inventory (calibration coefficients have been taken from the field book)
  1. Rename ki\_0000sav3\_000rug\_201102260930\_201104101410\_mez\_ra01\_nai05\_0000.asc to ki\_0000nkw1\_000rug\_201102260930\_201104101410\_mez\_ra01\_nai05\_0000.asc  since it has obviously been at nkw1 at that time and transferred to sav3 on 08.07.2011 (confirmed by mail from Juliane).
  1. Copy files from bin to asc. There are several wxt files which are only available in the bin folder (but in ascii format). These have been copied to the ra01 folder. In addition, the sav4 files have been renamed to sav0 (issue has been solved: the asc files have been in a separate folder because of the new generation of the data loggers - this has been done since julendat has not been adapted to it at that time):
```
ki_0000sav0_000wxt_201109120915_201109190815_mez_rb01_nai05_0000.bin
ki_0000sav0_000wxt_201109120915_201110051405_mez_rb01_nai05_0000.bin
ki_0000sav0_000wxt_201109120915_201110180805_mez_rb01_nai05_0000.bin
ki_0000cof3_000wxt_201109130020_201110170730_mez_rb01_nai05_0000.bin
```
  1. The following serial number/logger combinations are not in any file

  * 51021020182 (according to inventory rug on flm3, according to Tim's file on gra4) - the same starting time can also be found on gra02. Since gra4 is the only grassland plot where no 2010-12 record can be found at all, it is virtually certain the gra4 logger (gra1 had an interval of 2 seconds and therefore only 1.5 days recording; gra2, and gra5 have 2010-12 measurements, gra3 has been stolen all the time). Therefore we have changed the inventory to gra4.
  * 51021020195 (according to inventory rug on flm4)
  * 80081025282 (according to inventory pu1 on sav0 and was broken - deleted from inventory)
  1. One hourly measurements from logger 51021020150 have been moved from unresolved to the flm1 processing folder since the preliminary filename indicates flm1 and the logger id matches the information from the station inventory.
  1. Logger id 51021020176 has been set to sav4 from 2010-12-20 until 2011-02-18
  1. Logger id 51021020218 has been set to sav5 from 2010-12-15 until 2011-02-18


### Important ###

The following serial number/logger combinations are not in any file

  * 51021020182 (according to inventory rug on flm3, according to Tim's file on gra4)
  * 51021020195 (according to inventory rug on flm4)
  * 80081025282 (according to inventory pu1 on sav0 and was broken - deleted from inventory)

#### Solution for 51021020182 ####
According to inventory this rug should be on flm3, according to Tim's file on gra4. The same starting time can also be found on gra02. Since gra4 is the only grassland plot where no 2010-12 record can be found at all, it is virtually certain that this is the gra4 logger (gra1 had an interval of 2 seconds and therefore only 1.5 days recording; gra2, and gra5 have 2010-12 measurements, gra3 has been stolen all the time). Therefore we have changed the inventory to gra4.

#### Solution for 51021020195 ####
```
ki_0000flm4_000rug_201102240000_201103191820_mez_ra01_nai05_0000.asc
```
On February 24 2011, Tim has installed two loggers on two flm plots. He assumed that these plots are flm1 and flm2 but it turned out that flm2 (logger 51021020208) has actually been flm4 (see flm4 processing: the first file starting on 2011-02-24 has flm2 in the header, the following flm4). In the same way, it is virtually certain that the other logger (i. e. 51021020195) has not been installed on flm1 but on the neighboring flm3 plot. Hence, the logger file starting on 2011-02-24 with a header notice of flm1 are actually on flm3 and the one with flm2 are actually on flm4.The station inventory file has been updated accordingly.


```
ki_0000flm4_000rug_201103211600_201106251500_mez_ra01_nai05_0000.asc
ki_0000flm4_000rug_201106251510_201107091215_mez_ra01_nai05_0000.asc
```
Starting from 2011-03-21, the rug logger 51021020195 has obviously been moved to another plot. According to the station inventory it should have been flm4 (see autoplot notice in the bin filenames) but there are parallel and continues measurements available at flm4. Since these files are identical to the ones sent from Juliane as "flm5" files and the header of the logger file also mentions flm5, these files have been moved to flm5. The station inventory file has been updated accordingly.


## 2012-01-15 ##

### General ###
Process files which have been manually modified/sorted on 2012-01-07 to 2012-01-10.

  * ki\_0000gra0\_000rug\_201012200000\_201012210318\_mez\_ra01\_nas02\_0000.asc.gra0-or-gra1 (@gra0)
  * ki\_0000nkw1\_000pu1\_201103200900\_201103240810\_mez\_ra01\_nai01\_0000.asc.nkw1-or-cof3 (@nkw1)
  * ki\_0000nkw1\_000pu1\_201103241030\_201103271144\_mez\_ra01\_nai01\_0000.asc.nkw1-or-cof3 (@nkw1)
  * ki\_0000sav2\_000rug\_201110130900\_201111101035\_mez\_ra01\_nai05\_0000.asc.not-in-inventory (@sav2)

  * ki\_0000cof3\_000wxt\_201109130020\_201110170730\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000flm1\_000rug\_201102171000\_201102231900\_mez\_ra01\_nah01\_0000.asc
  * ki\_0000flm3\_000rug\_201102240000\_201103191820\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000flm5\_000rug\_201103211600\_201106251500\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000flm5\_000rug\_201106251510\_201107091215\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000gra4\_000rug\_201012141000\_201102240800\_mez\_ra01\_nai12\_0000.asc
  * ki\_0000mai0\_000pu1\_201104152200\_201109150820\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000mai0\_000wxt\_201104152200\_201107182200\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000sav0\_000wxt\_201104072200\_201104131225\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000sav0\_000wxt\_201109120915\_201109190815\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000nkw1\_000rug\_201102260930\_201104101410\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000sav4\_000rug\_201012201000\_201102181724\_mez\_ra01\_nai12\_0000.asc
  * ki\_0000sav5\_000rug\_201012151200\_201102180912\_mez\_ra01\_nai12\_0000.asc
  * ki\_0000sav0\_000pu1\_201110180810\_201111161205\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000mai0\_000wxt\_201104152200\_201109150730\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000sav0\_000wxt\_201104072200\_201104180950\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000sav0\_000wxt\_201104072200\_201108242315\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000sav0\_000wxt\_201109120915\_201110051405\_mez\_ra01\_nai05\_0000.asc
  * ki\_0000sav0\_000wxt\_201109120915\_201110180805\_mez\_ra01\_nai05\_0000.asc

## 2012-01-17 ##
Processing incoming dataset ki\_201111031159.7z without errors

server 002

## 2012-01-26 ##


  * ki\_201111080630.7z not processed (contains new Shira data)
  * ki\_201111121217.7z processed:

> ### Warning ###
> according to Ephraim fod2, but according to station inventory (german version) fod1
```
ki_0000fod2_rug_201109221310_201111081150_mez_ra01_nai05_0000.asc
```

  * ki\_201111211253.7z processed without errors (contains new Shira data)


## 2012-02-02 ##

  * ki\_201112131001.7z processed without errors (contains new Shira data)
  * ki\_201112311242.7z processed: **flm5 and sav4 serialnumber not in inventory**
> > ### Warning ###
> > according to Ephraim fod2, but according to station inventory (german version) fod1
```
ki_xx00fod2_000rug_201111081210_201112291050_mez_ra01_nai05_0000.asc
```
  * ki\_201201091324.7z processed:
> > ### Warning ###
> > no allocation by Ephraim, serialnumber not in inventory
```
ki_xx000000_xxx_201108171000_201111241245_mez_ra01_nai05_0000.asc.not_in_inventory
```
  * ki\_201201160658.7z processed:
> > ### Warning ###
> > according to Ephraim fod2, but according to station inventory (german version) fod1
```
ki_0000fod2_rug_201112291110_201201130305_mez_ra01_nai05_0000.asc
```


## 2012-02-06 ##

  * ki\_201201190851.7z processed
  * ki\_201201241320.7z not processed (contains only Shira data)

  * An error occured with the following datasets:
```
   ki_0000cof3_000rad_201110141100_201111280930_mez_ra01_nai05_0000.asc
   ki_0000cof3_000rad_201111281000_201112280840_mez_ra01_nai05_0000.asc
   ki_0000cof3_001rad_201110141120_201111280855_mez_ra01_nai05_0000.asc
   ki_0000cof3_001rad_201111280940_201112280820_mez_ra01_nai05_0000.asc
   ki_0000cof3_002rad_201110141120_201111280905_mez_ra01_nai05_0000.asc
   ki_0000cof3_002rad_201110141120_201112280815_mez_ra01_nai05_0000.asc
   ki_0000cof3_003rad_201110141140_201111280915_mez_ra01_nai05_0000.asc
   ki_0000cof3_003rad_201111281000_201112280830_mez_ra01_nai05_0000.asc
   ki_0000cof3_004rad_201110141140_201111280920_mez_ra01_nai05_0000.asc
   ki_0000cof3_004rad_201111281000_201112280835_mez_ra01_nai05_0000.asc
```

example:
**Exception args:  ("No section: '001rad\_header\_0000'",)**


## 2012-04-27 ##

  * ki\_201202071048.7z processed: conflicts: cof3, gra4, hom4 not in inventory; conflict directory copied in unresolved
  * ki\_201202142259.7z not processed (contains only Shira data)
  * ki\_201203080807.7z processed: conflicts: cof3, gra4, hom4, sav2, sav4 not in inventory; conflict directory copied in unresolved
  * ki\_201203300542.7z not processed: no data
  * ki\_201203301208.7z processed: conflicts: fod4, fod5, fpd5, fpo5 not in inventory; conflict directory copied in unresolved
  * ki\_201204161156.7z processed: conflicts: cof3, cof4, gra4, hom1, hom4, sav4 not in inventory; conflict directory copied in unresolved

  * An error occured with the following datasets:
```
   ki_0000cof3_000rad_201110141100_201111280930_mez_ra01_nai05_0000.asc
   ki_0000cof3_001rad_201110141120_201111280855_mez_ra01_nai05_0000.asc
   ki_0000cof3_002rad_201110141120_201111280905_mez_ra01_nai05_0000.asc
   ki_0000cof3_003rad_201110141140_201111280915_mez_ra01_nai05_0000.asc
   ki_0000cof3_004rad_201110141140_201111280920_mez_ra01_nai05_0000.asc
   ki_0000cof3_002rad_201110141120_201112280815_mez_ra01_nai05_0000.asc
   ki_0000cof3_001rad_201111280940_201112280820_mez_ra01_nai05_0000.asc
   ki_0000cof3_003rad_201111281000_201112280830_mez_ra01_nai05_0000.asc
   ki_0000cof3_004rad_201111281000_201112280835_mez_ra01_nai05_0000.asc
   ki_0000cof3_000rad_201111281000_201112280840_mez_ra01_nai05_0000.asc
   ki_0000cof3_002rad_201112280900_201201300750_mez_ra01_nai05_0000.asc
   ki_0000cof3_003rad_201112280900_201201300755_mez_ra01_nai05_0000.asc
   ki_0000cof3_004rad_201112280900_201201300800_mez_ra01_nai05_0000.asc
   ki_0000cof3_000rad_201112280900_201201300810_mez_ra01_nai05_0000.asc
   etc.
```

example:
**Exception args:  ("No section: '001rad\_header\_0000'",)**

## 2012-05-24 ##
  * Reprocessing of level 0050 files.
  * Prior to reprocessing, the conflict folder has been moved from plots/ki to unresolved.
  * Prior to reprocessing, the files within plots/ki haven been backuped to ki\_processing\_2012-05-24.7z

### Errors ###
  * The following files have not matching serial number:
```
0000cof1/ra01_nai05_0000/ki_0000cof1_000rug_201102180000_201102220655_mez_ra01_nai05_0000.asc
0000sav1/ra01_nai05_0000/ki_0000sav1_000rug_201103030830_201106271320_mez_ra01_nai05_0000.asc
```
  * The headers of the following radx files are not yet implemented (identical to errors on 2012-02-06 and 2012-04-27):
```
0000cof3/ra01_nai05_0000/ki_0000cof3_001rad_201110141120_201111280855_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_002rad_201110141120_201111280905_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_003rad_201110141140_201111280915_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_004rad_201110141140_201111280920_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_002rad_201110141120_201112280815_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_001rad_201111280940_201112280820_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_003rad_201111281000_201112280830_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_004rad_201111281000_201112280835_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_000rad_201111281000_201112280840_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_002rad_201112280900_201201300750_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_003rad_201112280900_201201300755_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_004rad_201112280900_201201300800_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_000rad_201112280900_201201300810_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_003rad_201201300808_201202290858_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_002rad_201201300830_201202290845_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_000rad_201201300815_201202290910_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_004rad_201201300830_201202290905_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_002rad_201202290930_201204030920_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_001rad_201202290935_201204030925_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_004rad_201202290935_201204030930_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_003rad_201202290935_201204030935_mez_ra01_nai05_0000.asc
0000cof3/ra01_nai05_0000/ki_0000cof3_000rad_201202290935_201204030940_mez_ra01_nai05_0000.asc
```


## 2012-07-10 ##

Reprocessing of files in conflict folder (ki\_process\_resort\_level0000). Resolved for all files except
  * Plot jul: ki\_xx000000\_xxx\_201108171000\_201111241245\_mez\_ra01\_nai05\_0000.asc.not\_in\_inventory
  * Plot sun:
    * ki\_xx000000\_xxx\_201112280930\_201201300620\_mez\_ra01\_nai05\_0000.asc.not\_in\_inventory
    * ki\_xx000000\_xxx\_201112281040\_201201300925\_mez\_ra01\_nai05\_0000.asc.not\_in\_inventory
    * ki\_xx000000\_xxx\_201201190830\_201201291345\_mez\_ra01\_nai05\_0000.asc.not\_in\_inventory
    * ki\_xx000000\_xxx\_201201300800\_201202290750\_mez\_ra01\_nai05\_0000.asc.not\_in\_inventory
  * Plot fpd5: ki\_xx00fpd5\_xxx\_201201200800\_201203181315\_mez\_ra01\_nai05\_0000.asc.not\_in\_inventory

Processing of level 0050 files.


## 2012-09-17 ##

Processing of files retrieved from C partition of hard disks from field laptops.
  * Pre-processed files (GUI processing performed at Nkweseko) have been copied to source folders
  * From those files, the dataset called "ki\_0000sav2\_000rug\_201109191340\_201110130255\_mez\_ra01\_nai05\_0000.asc" could not be processed since the serial number is not in the inventory.
  * Many files in conflict folder.

## 2012-12-21 ##
Over the last days, all available data have been reprocessed using the updated aggregation routines.
The level 0005 ascii files from the ongoing processing have been merged with those already available in the zip files within the incoming backup. The latter have been re-processed using the level 000 gui module.

The two initial data sets (ongoing and zip-re-process) and the resulting merged data set can be found in the processing backup path:
```
20102-12-20_gui_results_from_ongoing_ki.7z
2012-12-20_gui_results_from_zips_done_2012-12-20.7z
2012-12-20_merged_gui_results_from_2012-12-20.7z
```

The processed incoming zip files have all been stored within the `2012-12-20_level_0050_from_merged_gui_results.7z` directory of the incoming backup path.


## 2013-01-03 ##
Processing of the zip file from 24.12.2012 which has been sent manually due to a failure in the upload routine. The data has been reprocessed and merged into the operational processing stream.

## 2013-01-08 ##
Time corrections have been made for the first 1 to few month of 2011 where the loggers have been started with Tanzanian time in a MEZ computer environment. The logger time has been reduced by two hours for correction. The following plots have been corrected:
  * cof4
  * cof5
  * flm1
  * gra2
  * gra4
  * gra5
  * mai1
  * mai5
  * sav3
  * sav4
  * sav5


## 2013-01-08 ##
Time corrections have been made for the last 1 to few month of 2012 where the loggers have time sync problems. The following plots have been corrected (times are in MEZ!):
  * hom1: deleted 2011-12-29 00:00 to 2012-01-16 16:25
  * hom1: + 8 hours, starting from 2012-10-27 01:00
  * hom2: + 6 hours, starting from 2012-11-08 10:10
  * hom5: deleted 2012-10-26 20:00 to 2012-11-21 09:40
  * sav2: deleted 2011-12-22 19:00 to 2012-01-10 08:15 (EOF, serial number: 051021020183). Part of this time frame could be filled using a second logger which has been installed on the plot on 2011-12-27 09:00 (051021020188)
  * gra2: File ki\_0000gra2\_000rug\_201110211130\_201111140045\_mez\_ra01\_nai05\_0000 has been split on 2011-11-07 19:25 and the remaining data set has been corrected by -5 hours (2011-11-08 11:30 to 2011-11-14 16:45; there has been a gap of 22 hours starting from 2011-11-07 19:25)

File `ki_0000hom2_000rug_201210040920_201210090525_mez_ra01_nai05_0000.asc`
is corrupt and has been deleted.

## 2013-03-13 ##

### General ###
  1. The following zip-files were processed with the version f0d76dbed05d:   `ki_201301311130.7z`, `ki_201302021439.7z`,`ki_201303061105.7z` See warning reason **1**.
  1. A backup file has been created afterwards:  **ki\_processing\_plots\_2013-03-13.7z**



### Warning ###

There were five errors by the processing calibration 0050. These errors have been made because the sensors number (par or swdr)  were not written into the 'ki\_config\_stations\_inventory.cnf' file. This information should be conveyed on site and entered in the config file (ROW- PYR01,SERIAL\_PYR02,SERIAL\_PAR01,SERIAL\_PAR02)

```
ki_0000fod2_000rad_201210261100_201212031255_mez_ra01_nai05_0000.asc
ki_0000fod2_000rad_201212031310_201302110825_mez_ra01_nai05_0000.asc
ki_0000fpo1_000rad_201210122200_201211260850_mez_ra01_nai05_0000.asc
ki_0000foc6_000rad_201210171400_201211261215_mez_ra01_nai05_0000.asc
ki_0000mch0_000rad_201210122200_201211260805_mez_ra01_nai05_0000.asc
```

Exception Content
```
Original level 0000 headers:  ['Date', 'Time', 'Temperature   [\xb0C]', 'rel.Humidity   [%]', 'Voltage DVM   [mV]', 'Voltage DVM   [mV]', '']
An error occured with the following dataset.
Some details:
Filename: /home/eikistations/ei_data_kilimanjaro/processing/plots/ki/0000fod2/ra01_nai05_0000/ki_0000fod2_000rad_201212031310_201302110825_mez_ra01_nai05_0000.asc
Exception type:  <type 'exceptions.UnboundLocalError'>
Exception args:  ("local variable 'level_0000_column_headers' referenced before assignment",)
Exception content:  local variable 'level_0000_column_headers' referenced before assignment
```

Ephraim has been notified to instruct Jimmy to record the rad-sensor serial numbers for the above mentioned plots. The station inventory will be updated accordingly when this info is available. This should resolve the above mentioned issues.

## 2013-11-08 ##
After an error in the configuration file settings, level 0000 to level 0050 file names have been finally corrupted. Today, the state of 08/06/2013 has been recovered. All incoming files (...83) have been copied to backup/incoming\_backup. For the next processing, the files which have not been processed until 08/06/2013 have to be identified. In case of doubt, reprocessing of the files is recommended.

## 2013-11-26 ##
All files up to 2013-11-12 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing\_backup (ki\_processing\_plots\_2013-11-26.7z)

## 2013-12-10 ##
All files up to 2013-12-05 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing\_backup (ki\_processing\_plots\_2013-12-05.7z)

## 2014-01-21 ##
All files up to 2014-01-20 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing\_backup (ki\_processing\_plots\_2014-01-20.7z)

## 2014-02-06 ##
All files up to 2014-02-06 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing\_backup (ki\_processing\_plots\_2014-02-06.7z)

## 2014-02-20 ##
All files up to 2014-02-20 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing\_backup (ki\_processing\_plots\_2014-02-20.7z)

## 2014-04-02 ##
All files up to 2014-04-02 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing\_backup (ki\_processing\_plots\_2014-04-02.7z)

## 2014-05-14 ##
All files up to 2014-05-14 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing\_backup (ki\_processing\_plots\_2014-05-14.7z)

## 2014-05-22 ##
Update station\_inventory

## 2014-05-27 ##
All files up to 2014-05-27 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing (ki\_processing\_plots\_2014-05-27.7z)

## 2014-06-08 ##
All files up to 2014-06-08 have been processed up to final level 0415. Complete processing/plots/ folder  zipped and saved in backup/processing (ki\_processing\_plots\_2014-06-08.7z)

## 2014-06-12 ##
Deleted all content of processing/plots/ki folders. Unzipped last 2 incoming ZIP-files and reprocessed up to level0200.

## 2014-06-13 ##
"No such file or directory" Error in level0200, couldn't find level0190 files -> some R-Packages were missing -> FIXED

## 2014-06-14 ##
All files up to 2014-06-12 have been processed to final level 0415 (without any erros!). Complete processing/plots/ folder  zipped and saved in backup/processing (ki\_processing\_plots\_2014-06-14.7z)

## 2014-06-16 ##
Update ki\_station\_inventory (cof3 wxt & swapped last 4 entries of lines 20 and 21)

## 2014-06-18 ##
All files up to 2014-06-18 have been processed to final level 0415 (without any erros!). Complete processing/plots/ folder  zipped and saved in backup/processing (ki\_processing\_plots\_2014-06-18.7z)

## 2014-07-03 (pastprocessing) ##
Error messages in level0050 occured. Fixed station\_inventory, started ki\_prepare\_reprocess\_level0050.py, copied whole ki/plots/ - folder into incoming - folder and started ki\_preocess\_resort\_level0000.py

## 2014-07-11 (pastprocessing) ##
All files have been processed to final level 0415. Complete processing/lots/ folder zipped and saved in backup/processing (ki\_processing\_plots\_2014-07-11.7z)

## 2014-07-11 ##
All files up to 2014-07-11 have been processed to final level 0415 (without any erros!). Complete processing/plots/ folder  zipped and saved in backup/processing (ki\_processing\_plots\_2014-07-11.7z)

## 2014-07-18 (pastprocessing) ##
Reprocess data starting from level0200. Not all files have been processed further than level0190 in last full processing run.

## 2014-07-25 (pastprocessing) ##
Remove all processing levels but level0000, run ki\_prepare\_reprocess\_level0050.py, move all _.asc_ to /incoming/ and delete content of /processing/plots/ki/. Remove 2013 & 2014 files and start reprocess all 2011 & 2012 data.

## 2014-07-25 ##
Start processing latest files ki\_20140721

## 2014-07-27 (pastprocessing) ##
All files 2011 + 2012 have been processed to final level 0415 (without any erros!). Create Backup ki\_pastprocessing\_plots\_2014-07-27.7z

## 2014-07-28 ##
All files 2013 + 2014 have been processed to final level 0415 (without any erros!). Create Backup ki\_processing\_plots\_2014-07-28.7z

## 2014-08-14 ##
Uploaded files (rug + pu1 logger) 2011-2014 to Kilimanjaro Main Database (Würzburg)

## 2014-08-19 ##
Start processing latest files ki\_20140801 and ki\_20140811

## 2014-08-28 ##
All files up do 2014-08-28 have been processed up to final level 0415 (no errors). Backup-file created ki\_processing\_plots\_2014-08-28.zip

## 2014-09-08 ##
Several plots were missing in processing/plots/ki -> copied last backup-files (2014-08-28)

## 2014-09-15 ##
All files up do 2014-09-15 (last file: ki\_20140908) have been processed up to final level 0415 (no errors). Backup-file created ki\_processing\_plots\_2014-09-15.zip

## 2014-09-28 ##
All files up do 2014-09-28 (last file: ki\_20140919) have been processed up to final level 0415 (no errors). Backup-file created ki\_processing\_plots\_2014-09-28.zip

## 2014-10-13 ##
Start processing latest files ki\_20141006 & 20141010

## 2014-10-15 ##
All files up do 2014-10-15 (last file: ki\_20141010) have been processed up to final level 0415 (no errors). Backup-file created ki\_processing\_plots\_2014-10-15.zip

## 2014-10-21 ##
Local HDD Backup ki\_processing & ki\_pastprocessing

## 2014-10-26 ##
All files up do 2014-10-26 (last file: ki\_20141021) have been processed up to final level 0415 (no errors). Backup-file created ki\_processing\_plots\_2014-10-26.7z

## 2014-10-28 ##
Local HDD Backup ki\_processing & ki\_pastprocessing

## 2014-11-02 ##
All files up do 2014-11-02 (last file: ki\_20141030) have been processed up to final level 0415 (no errors). Backup-file created ki\_processing\_plots\_2014-11-02.7z

## 2014-11-03 ##
Local HDD Backup ki\_processing & ki\_pastprocessing

## 2014-11-04 ##
No new incoming files since beginning of 05-2014. All weekly zip-files have the same filesize since may.

## 2014-11-17 ##
Update / Debug station\_inventory. Start to reprocess all initial files.

## 2014-11-23 ##
All files up do 2014-11-23 (last file: ki\_201411150000\_reprocessAllInitialFiles.7z) have been processed up to final level 0415 (no errors). Backup-file created ki\_processing\_plots\_2014-11-23.7z

## 2014-12-06 ##
Start processing ki\_20141205-100246.7z

### level0050 ###
**Error occured** with following file:

```
ki_0000fer0_000rad_201409021600_201409292355_mez_ra01_nai05_0000.asc
Exception type:  <type 'exceptions.ValueError'>
Exception args:  ("'radx' is not in list",)
Exception content:  'radx' is not in list
```

## 2014-12-08 ##
All files up do 2014-12-08 (last file: ki\_20141205-100246s.7z) have been processed up to final level 0415 (no errors). Backup-file created ki\_processing\_plots\_2014-12-08.7z
Created visualization for level0050 and level0290 2014 files.