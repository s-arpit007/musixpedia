# musixpedia

This is a utility app for Spotify with personalised recommendations based on our algorithm for song recommendation.
It will also provide you different kind of insights into your listening behaviour.

### How to run this application?
1. Clone the repository in your machine using `git clone`
   ```buildoutcfg
    musixpedia
    |__.env
    |__requirements.txt
    |__run.py
    |__server.wsgi
    |__README.md
    |__app
       |____init__.py
       |__home.py
       |__utils.py
       |__static
       |__templates
          |__index.html
          |__home.html
          |__layout.html
   ```
2. Create a `.env` file inside musixpedia repository containing below environment variables
   ```buildoutcfg
     export SPOTIPY_CLIENT_ID= 'your client id'
     export SPOTIPY_CLIENT_SECRET= 'your client secret'
     export SPOTIPY_REDIRECT_URI= 'redirect uri'
     export FLASK_APP= 'app/home.py'
   ```
   if you are running on development server, add below line as well in the `.env`
   ```buildoutcfg
     export FLASK_ENV=development
   ```
3. Install requirements from `requirements.txt`
4. Now go to musixpedia directory and run below command:
    ```buildoutcfg
      flask run
    ```
    or
    ```buildoutcfg
      python run.py
    ```
   
After, following above steps you should see the output similar to below

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