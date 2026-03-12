# Capture Service Specification

Module:
CaptureService

Function:
captureVisibleTab()

Purpose:
Capture the currently active browser tab.

Input:
none

Output:
PNG image data (base64)

Behavior:

1
Get active tab

2
Call chrome.tabs.captureVisibleTab

3
Return base64 image

Errors:

Capture failure
Permission error

Constraints:

Must run in background context