### This repository contains: 
- ### a collection of tools that reduce manual work in testing, data analysis, and product validation;
- ### python libraries for files, images and logs processing.

# Tools:

## Events to graph timeline builder
If you have a bunch of events and images related to the events with timestamps, you can build a graphic timeline or several timelines on the time scale.
[More](https://www.scirra.com/)

## Screenshoter

## Simple UI test starter

## Video events and recorder

## SVC checker (for windows)

# Libraries

## files
## images
## logs


## Table of Contents
- [FilesLib.py](#fileslibpy)
- [ImagesLib.py](#imageslibpy)
- [ParsedLog.py](#parsedlogpy)
- [GraphTimeLine.py](#graphtimelinepy)
- [SVC Checker](#svc-checker)
- [VideoEventsCounter](#videoevents-counter)
- [Screenshoter](#screenshoter)

## FilesLib.py

Library for handling files and folders (list files, copy files, clear folders, etc.).

## ImagesLib.py

Library for handling Images (find different images, blend images, etc.).

### Feature Highlight: Image Filtering

You can filter your images to find specific pictures using the function:

```python
def copyDifferentImages(folderForScanningImages, folderForResImages, filterPercent)
```

This function allows you to identify and copy images that differ by a specified percentage. Here's an example of the output:

![filter_img screenshot](/Content/filter.png?raw=true "Screenshot")

## ParsedLog.py

A simple class for handling logs.

## GraphTimeLine.py

A tool for comparing results on a timescale. This is particularly useful when you need to compare different versions of your project over time.

### Usage Example

Use the `autovision_v1` and `autovision_v2` folders to see how GraphTimeLine works. Here's a screenshot of the output:

![GraphTimeline screenshot](/Content/GraphTimeLineImg.png?raw=true "Screenshot")

## SVC Checker

A simple but useful tool to show which Windows services have stopped running. This is particularly convenient for testing Windows applications that create their own services.

### Features
- Created using [Scirra Construct 2](https://www.scirra.com/)
- Easy to customize for your specific services

### Customization
1. Edit the project with Scirra Construct 2
2. Overwrite the batch files according to your services

![svc_checker](/Content/svc_checker.png?raw=true "Screenshot")

## VideoEvents Counter

An application created with [Scirra Construct 2](https://www.scirra.com/) to streamline the process of logging events in video content. This tool can significantly increase work efficiency, especially when dealing with event-heavy videos (e.g., autopilots, conveyors, crowded scenes).

### Features
- Add and drag & drop green markers
- Record up to 4 counters
- Easily extendable functionality using Construct 2

![VideoEventsCounter](/Content/VideoEventsCounterScreenshot.png?raw=true "Screenshot")

## Screenshoter

This is a custom screenshoter script that can save your screenshots according to calling parameters and has all standard editing features.

### Features
- Save screenshots based on custom parameters
- Standard editing capabilities:
  - Draw arrows, rectangles, bars
  - Add text
  - Blur specific areas
  - Cut images
  - Undo changes
  - Chose colors

---
