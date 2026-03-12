# Project

Chobi Screenshot Extension

Description:
Browser extension that captures the current webpage screenshot and saves it using customizable filename templates and optional subfolders.

Target Browser:
Google Chrome (Manifest V3)

---

# File Structure

```
src/

manifest.json

background/
  background.ts

services/
  CaptureService.ts
  FileNameService.ts
  SettingsService.ts
  DownloadService.ts

options/
  options.html
  options.ts
  options.css
```

Build output:

```
dist/

manifest.json
background/background.js
services/*.js
options/options.js
```

---

# Extension Manifest

File:
src/manifest.json

Key Configuration:

```
manifest_version: 3

name: Chobi Screenshot Extension
version: 1.0

permissions:
- tabs
- downloads
- storage
- activeTab

background:
  service_worker: background/background.js

options_page: options/options.html

action:
  default_title: Capture Screenshot
```

---

# Modules

---

## Capture Module

Responsibility:
Capture the currently visible browser tab.

Files:
src/services/CaptureService.ts

API:

captureVisibleTab()

Inputs:
none

Outputs:
image dataURL (PNG)

Implementation:
Uses chrome.tabs.captureVisibleTab

Dependencies:

chrome.tabs
chrome.tabs.captureVisibleTab

---

## File Naming Module

Responsibility:
Generate a filename from a template string and page metadata.

Files:
src/services/FileNameService.ts

API:

generateFileName(template, metadata)

Inputs:

template (string)

metadata object:

```
{
  url: string
  title: string
  date: Date
  counter: number
}
```

Outputs:

filename string

Supported Template Tokens:

```
%n  counter
%t  page title
%u  page url
%y  year
%m  month
%d  day
%H  hour
%M  minute
```

Example:

```
Capture %n - %t - %y%m%d
```

Dependencies:
none

---

## Settings Module

Responsibility:
Store and retrieve user configuration.

Files:
src/services/SettingsService.ts

API:

getSettings()

saveSettings(settings)

Inputs:

settings object

Outputs:

settings object

Settings Structure:

```
{
  imageType: "png" | "pdf",
  fileNameTemplate: string,
  subFolder: string
}
```

Default Settings:

```
{
  imageType: "png",
  fileNameTemplate: "Capture %n - %t",
  subFolder: "Chobi"
}
```

Dependencies:

chrome.storage

---

## Download Module

Responsibility:
Save captured image data to the user's computer.

Files:
src/services/DownloadService.ts

API:

downloadImage(dataURL, filename, folder)

Inputs:

dataURL (string)
filename (string)
folder (string)

Outputs:

file saved via browser download

Implementation:

Uses chrome.downloads.download

Dependencies:

chrome.downloads

---

## UI Options Page Module

Responsibility:
Provide user interface for configuring extension settings.

Files:

src/options/options.html
src/options/options.ts
src/options/options.css

Features:

Image format selection

* PNG
* PDF

Subfolder configuration

Filename template configuration

Save button

Dependencies:

SettingsService

---

## Background Module

Responsibility:
Coordinate extension behavior when the user triggers a screenshot.

Files:

src/background/background.ts

Trigger:

User clicks extension toolbar icon.

Flow:

1 User clicks extension icon
2 Background receives click event
3 SettingsService.getSettings()
4 CaptureService.captureVisibleTab()
5 FileNameService.generateFileName()
6 DownloadService.downloadImage()

Dependencies:

CaptureService
FileNameService
DownloadService
SettingsService

---

# Data Flow

User Action:

Click extension toolbar icon

System Flow:

Background Script

↓

Load settings

↓

Capture visible tab

↓

Generate filename

↓

Download image

---

# Permissions

Required Chrome Permissions:

tabs
downloads
storage
activeTab

---

# Error Handling

Possible Errors:

Capture failure
Download
