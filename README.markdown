rollcall
========

Exploring the people and mailing lists at GDS.


Setup
-----

Check out this repo, then put the relevant `client_secrets.json` and 
`tokens.dat` files in the root, otherwise you won't be able to read
from the Google Admin API.

Then:

    mkvirtualenv rollcall
    workon rollcall
    pip install -r requirements.txt
    python manage.py syncdb --migrate
    python manage.py load_people
    python manage.py load_groups
    python manage.py load_memberships

