# musixpedia

This is a utility app for Spotify with personalised recommendations based on our algorithm for song recommendation.
It will also provide you different kind of insights into your listening behaviour.

### Setup on your local Ubuntu machine
1. Clone the repository in your machine using `git clone`
   ```buildoutcfg
   musixpedia/
      |__.env
      |__requirements.txt
      |__run.py
      |__server.wsgi
      |__README.md
      |__app/
         |____init__.py
         |__home.py
         |__utils.py
         |__static/
         |__templates/
            |__index.html
            |__home.html
            |__layout.html
   ```
2. Create a `.env` file (at musixpedia/.env) inside musixpedia repository containing below environment variables
   ```buildoutcfg
   export SPOTIPY_CLIENT_ID='your client id'
   export SPOTIPY_CLIENT_SECRET='your client secret'
   export SPOTIPY_REDIRECT_URI='redirect uri'
   export FLASK_APP='app/home.py'
   export FLASK_ENV=development
   ```
   if you are running on development server, add below line as well in the `.env`
   ```buildoutcfg
   export FLASK_ENV=development
   ```
3. Install requirements from `requirements.txt`
   ```buildoutcfg
   pip install -r requirements.txt
   ```
4. Now go to musixpedia directory and run below command:
    ```buildoutcfg
    flask run
    ```
    or
    ```buildoutcfg
    python run.py
    ```
   
After following above steps you should see the output similar to below

      > Serving Flask app "app" (lazy loading)
      > Environment: development
      > Debug mode: on
      > Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
      > Restarting with stat
      > Debugger is active!
      > Debugger PIN: 152-577-664

Always keep your redirect uri at a different port then application port to make login with spotify work. Like in this example
```buildoutcfg
   application_url = http://127.0.0.1:5000/
   redirect_url = http://127.0.0.1:8080/
```
Otherwise, if you keep them at the same port, you will get an error saying _Address already in use_ and your login will fail.

### Set up with Apache2 on Ubuntu
1. Installation of required linux packages.
   ```commandline
   sudo apt-get remove --purge apache2 apache2-data apache2-utils
   sudo apt-get install apache2
   sudo apt-get install python3-pip
   sudo pip3 install virtualenv
   sudo apt-get install libapache2-mod-wsgi-py3
   ```
2. Check the installation of apache2 by below command. It should be in running status and should return the standard `index.html` at `http://localhost`.
   ```commandline
   sudo /etc/init.d/apache2 status
   ```
   You can stop/restart/start the apache2 service with below commands
   ```commandline
   sudo /etc/init.d/apache2 status
   sudo /etc/init.d/apache2 restart
   sudo /etc/init.d/apache2 start
   sudo /etc/init.d/apache2 stop
   ```
   or 
   ```commandline
   sudo systemctl status apache2.service
   sudo systemctl reload apache2.service
   sudo systemctl stop apache2.service
   sudo systemctl start apache2.service
   ```
3. Install python specific packages
   ```commandline
   sudo virtualenv venv
   source venv/bin/activate
   sudo pip3 install -r requirements.txt
   deactivate
   ```
4. Set up required environement variables in `/etc/apache2/envvars`.
   ```commandline
   export SPOTIPY_CLIENT_ID='your client id'
   export SPOTIPY_CLIENT_SECRET='your client secret'
   export SPOTIPY_REDIRECT_URI='redirect uri'
   ```
5. Clone the code at `/var/www/musixpedia/`
   ```buildoutcfg
   /var/www/musixpedia/
            |__requirements.txt
            |__run.py
            |__server.wsgi
            |__README.md
            |__app/
            |____init__.py
            |__home.py
            |__utils.py
            |__static/
            |__templates/
               |__index.html
               |__home.html
               |__layout.html
   ```
6. Configure a new application with apache2
   ```commandline
   sudo nano /etc/apache2/sites-available/musixpedia
   sudo nano /etc/apache2/sites-available/musixpedia.conf
   ```
   Add below configurations in the conf file. Replace relevant values according to your environment. 
   ```commandline
   <VirtualHost *:80>
      ServerName localhost
      ServerAdmin admin@mywebsite.com
      WSGIDaemonProcess   python-path=/home/arpit/anaconda3/bin/python/site-packages
      WSGIScriptAlias / /var/www/musixpedia/server.wsgi
      <Directory /var/www/musixpedia/app/>
         Order allow,deny
         Allow from all
      </Directory>
      Alias /static /var/www/musixpedia/app/static
      <Directory /var/www/musixpedia/app/static/>
         Order allow,deny
         Allow from all
      </Directory>
      ErrorLog ${APACHE_LOG_DIR}/error.log
      LogLevel warn
      CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>
   ```
   Then, reload your apache2 instance.
   ```commandline
   sudo service apache2 restart
   sudo systemctl reload apache2.service
   ```
   Now, you should be able to see the site at `http://localhost/`
* You can find the error/service logs at `/var/log/apache2/`

#### TODO
1. URI redirect for spotify login is not working in apache mode. Error: Address already in use.
2. Add new features to make this site useful.