## PigyBank -Reporting and Transaction (By Isreal Ogbu, Fagbemi Ayomide)

This is a project that is mainly built for the #APISecurityHackathon. We are also looking forward to building more sub applications on it.

The project for the hackathon challenge will be mainly focussed on Authentication, Authorization, Reporting customer feedback (Notification, Enquiry) and Investment section(APIs).
For the sake of the hackathon, we will not be using any third party databse. We will be taking advantage of the
Database provided by Django (Sqlite).
***

## Tools to ensure the solution runs effectively
***

Ensure you have `Vscode` or `Pycharm` installed on your machine.

Also ensure you have `pip` installed. This is a package installer for python.

create a subdirectory for the project, and move into the directory either on pycharm or vscode.

Create a virtual environment by running :

For windows: `venv/scripts/activate`
For Mac : `source venv/bin/activate`

Once the above  is installed and done, You set for the project.
***
## How to Install and run pigybank project.
***
To run Pigybank project on your machine:
1. Initialize your directory with git by running : `git init`
2. create a branch for the project by running : `git branch -m <you branch name>`. This can be optional if you want solve some issues 
3. Clone this repository by running : `git clone https://github.com/Isreal-ogbu/pigybank`
4. To install packages and dependencies, run: `pip install -r requirements.txt`

Before running projects, There are some environmental variables that you will need to set.
create a file, call it `.env`. Input the below with appropriate values:

1. `SECRET_KEY`
2. `TREBLLE_API_KEY`
3. `TREBLLE_PROJECT_ID`

**Note: There are some variables in the .env file which can be set to `null`.
1. RAVE_PUBLIC_KEY = null 
2. RAVE_SECRET_KEY = null
3. DEFAULT_PASSWORD = ''
***
We intend implementing a payment solution for the project, but we decided not to due to the complexity.
The entire end points from the `user_payment` app is no more meant for the hackathon.
***
#### Available endpoints are:

localhost:8000 or 127.0.0.1:8000/

1. api/c/catagories/
2. api/c/transactions/
3. api/c/currencies/
4. api/c/report/
5. api/u/register/
6. api/u/login/
7. api/u/logout/
8. api/u/verify-email/
9. api/n/notification/ 
10. api/u/set-password/ ......and lot more.

** Please note again: The `user_payment` applications urls are not currently working.
***

