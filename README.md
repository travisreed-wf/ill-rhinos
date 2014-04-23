Illustrious Rhinoceroses Group Project
==========
[ill-rhinos.appspot.com](http://ill-rhinos.appspot.com/)

Setting Up
-----------
* Download and Install [Python 2.7](http://www.python.org/download/releases/2.7/)
* Download and Install [GAE Python SDK](https://developers.google.com/appengine/downloads)
* Download and Install [Git](http://git-scm.com/book/en/Getting-Started-Installing-Git)
* Checkout this repository ```git clone https://github.com/theMagicalKarp/uptown-prototype.git uptown```
* Start GAE SDK and select this project.

Libraries and Frameworks Used
-----------
* [Google App Engine](https://developers.google.com/appengine/) *Web framework for running our python enviroment*
* [Flask](http://flask.pocoo.org/) *URL Routing*
* [Jinja2](http://jinja.pocoo.org/) *HTML templating*
* [Bootstrap](http://getbootstrap.com/) *HTML Styling*
* [jQuery](http://jquery.com/) *Wrapper for JavaScript... Also required for bootstrap... D:*

What's Going On?!
-----------
[__/app.yaml:__](https://github.com/theMagicalKarp/ill-rhinos/blob/master/app.yaml) Basic config that Google App Engine uses to understands how to run our application. This is the first thing ran when starting the server.

[__/libs/:__](https://github.com/theMagicalKarp/ill-rhinos/tree/master/libs) Contains external python libraries such as Flask, werkzeug, ect...

[__/app/views.py:__](https://github.com/theMagicalKarp/ill-rhinos/blob/master/app/views.py) Contains instructions of how to map our application to specific urls.

[__/app/templates/:__](https://github.com/theMagicalKarp/ill-rhinos/blob/master/app/templates) This directory holds html template files that are to be rendered by jinja2.  Each html file extends a base html file that describes how each page should look.  This helps enforce consistancy among all of the pages.  You can find out more about jinja2 templating [here](http://jinja.pocoo.org/docs/templates/).

[__/static/data/*.json:__](https://github.com/theMagicalKarp/ill-rhinos/tree/master/static/data)  This directory holds json serialized information about current courses offered at Iowa State University by major.

[__/scripts/isu_scraper.py:__](https://github.com/theMagicalKarp/ill-rhinos/blob/master/scripts/isu_scraper.py)  This is a python script that scrapes the [Iowa State class](http://classes.iastate.edu/) webiste and serliazes the classes into json files in the static data directory.
