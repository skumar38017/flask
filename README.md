# Required ( on ubuntu )
        sudo apt-get install python3 -y
        sudo apt install python3-full -y
        sudo apt install python3-pip -y
        sudo apt install pipx -y
        sudo apt install python-is-python3 -y
        sudo apt install python3-flask -y
        sudo apt install python3-selenium
        sudo apt install python3-openpyxl -y

# install google-chrome on ubuntu
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo dpkg -i google-chrome-stable_current_amd64.deb
        sudo apt-get install -f
        which google-chrome


        
# 1. Create a folder 
        mkdir flask_app
        cd flaskapp
        
# 2. clone from git 
        git clone https://github.com/sumitkumar74604/flask.git

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
