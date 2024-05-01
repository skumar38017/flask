# flask
# 1. Create a folder 
        mkdir flask_app
        cd flaskapp
# 2. clone from git 
        git clone https://github.com/sumitkumar74604/flask.git
        sudo apt-get install python3 

# create virtual virtual env  ( if you want run on local Machine ( Ubuntu/window))
        python -m venv flaskAppSite
        source/flaskAppSite/bin/activate (ubuntu)
        cd flaskAppSite/script activate

# 3. install requriments.txt file 
        pip install -r requriments.txt

# 4. run application
        python app.py 
# 5. Correct Chrome Binary Permissions
        sudo chmod +x /usr/bin/google-chrome
        sudo chmod +x path/to/chromedriver 
        sudo chmod +x path/to/chromedriver.exe

# . Go to Postman and apply GET method 
        http//:127.0.0.1:5000
