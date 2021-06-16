# The Pitcherr
#### Pitcherr, 2021.
#### By **Peter Kennedy**
## Description
A Flask powered application where the user can:
- Post a one minute pitch on any category among the listed.
- View, like and comment on other people's pitches.
- Create an account and view own profile.

The site is deployed on Heroku.

## Setup/Installation
On your terminal, clone the project.
    
    $ git clone git@github.com:peterken674/pitcher.git

Navigate into the cloned project.

    $ cd pitcher

Create a `start.sh` file.

    $ touch start.sh

Inside `start.sh`, addv the following. The email will be used to send welcome emails to new users who sign up, Gmail is recommended.

```bash
#!/bin/sh
export FLASK_ENV=development
export MAIL_USERNAME=<YOUR_EMAIL>
export MAIL_PASSWORD=<EMAIL_PASSWORD>
export SECRET_KEY=<SECRET_KEY>

python3 manage.py server
```

Create the virtual environment and install the requirements from `requirements.txt`

    $ python3 -m venv virtual
    $ . virtual/bin/activate
    $ pip install -r requirements.txt

Give the `start.sh` file execution permissions.

    $ chmod a+x start.sh

Run the program.

    $ ./start.sh
## Known Bugs
- Sign up redirect to login page sometimes fails but the user is created anyway.
## Technologies Used
- Flask(Python)
- Jinja2
- Unittest
## Support and contact details
If you have any suggestions, questions or in case of a fire, you can reach the developer via [email](mailto:peterken.ngugi@gmail.com).
### License
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Copyright &copy; 2021 **[peterken674](www.github.com/peterken674)**