Max Saunders Pottery Website
============================
I'm developing using Python 3.4.1, but it should be compliant with
earlier versions as well.

To run, it's highly recommended to create a virtual environment.
```
pyvenv ./env/
source env/bin/activate
```

Now, all the requirements can be installed easily by using
```
pip install -r requirements.txt
```

Now that we've got the requirements, run the server with
```
./run.py
```

All routes should be up!

API Documentation can be accessed at http://localhost:8000/api/.

The stuff I want you to work on, Moawia, is the admin page (/admin),
whose HTML file can be found at sand/static/templates/admin/index.html.
The route is already being served by Flask, and I've included and setup
angular to run using the application file sand/static/js/app/admin-app.js.

Good luck!
