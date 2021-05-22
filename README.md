# AirWatch-API
Examples of REST API Methods

Several typical functions of working with REST API:

* Searching for devices in a tenant
* Filtering devices by OS (Win/Linux)
* Getting a list of tags for the tenant
* Scanning a file with list of Notebook/Smartphone/Tablet serial keys, then checking if enrolled devices have such serials, and writing the result in a file
* Assigning devices to a chosen tag

Linked [portal KB page](https://digital-work.space/display/AIRWATCH/AirWatch+REST+API+Python+Examples)

Code is for Python version 3.7+, no dependencies (except it needs VMware Workspace ONE UEM to be installed of course) and is bundled into a dataclass as methods, with error-catching and logging support.
