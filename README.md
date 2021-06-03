# Tools

Here I am going to post some part of my framework, which is making live, development and tests easier.

## FilesLib.py 

Library for handling files and folders (list files, copy files, clear folders ...)

## ImagesLib.py 

Library for handling Images (find different images, blend images ...)

For instance, you can filter you images to find some specific pictures with function:
```
def copyDifferentImages(folderForScanningImages, folderForResImages, filterPersent)
```
The result of the function is like this (see the screenshot below)

<br>

![filter_img screenshot](/Content/filter.png?raw=true "Screenshot")

## ParsedLog.py 

Very simple class for handling logs.

## GraphTimeLine.py 

The tool for comparing results on a timescale. For example use autovision_v1 and autovision_v2 folders to see, how GrapTimeline working is. See the screenshot below.

<br>

![GrapTimeline screenshot](/Content/GraphTimeLineImg.png?raw=true "Screenshot")

## svc checker 

Using Scirra Construct 2 [Scirra Construct 2](https://www.scirra.com/) I created a very simple but absolutely useful tool to show you which Windows service felt down. Very convinient to test with, if your Windows application makes it's own services.

<br>

![svc_checker](/Content/svc_checker.png?raw=true "Screenshot")
