
# SwipeX
A simple online marketplace to exchange dining hall swipes here at UCLA.

## Directory Structure
Backend and Frontend code can be found in their respective folders.
#### Backend
* `backend/api/` is where most backend development is done
* Serializers are found in this folder, in `serializers.py`
* to add a new endpoint, add the url to `url.py`
and implement the function in either a new or existing view file, e.g. `swipeviews.py`

#### Frontend
* the xCode project files are found in this directory

## Installation/Run instructions
* Frontend is in Swift for an iOS app, so you should clone the files and run the project in XCode.
* Backend is implemented in Django, and we recommend a Python virtual environment with version >= 3.5
* `pip install -r requirements.txt`
* After a recent pull, run the following commands
	* `python manage.py makemigrations api`
	* `python manage.py migrate`
* To run the server, run
	*  `python manage.py runserver`

## Relevant Links
- Database
	- hosted at [https://www.mongodb.com/cloud](https://www.mongodb.com/cloud)
- Documentation link
- Working URL (if any)
- anything else

## Team
Ashwin Vivekanandh
Eric Dang
Jonathan Schwartz
Taasin Saquib
Xuesen Cui
