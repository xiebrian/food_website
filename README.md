# Setup / Installation

### MacOS 11.1 Setup / Installation

```
# First, create a Django virtual environment
sudo pip install virtualenv
# Create and activate a virtual environment for Django
sudo pip install django==2.2.10
python -m django --version

# Install all relevant dependencies:
brew install libjpeg
sudo pip install Pillow
sudo pip install easy-thumbnails
sudo pip install dj-database-url
sudo pip install django-image-cropping
sudo pip install django-storages
sudo pip install django-tables2
sudo pip install python-dateutil

# ...TODO (how to actually run it locally)

# Install Heroku
brew tap heroku/brew && brew install heroku
```

### Making changes

```
# Deploy the changes to Heroku
heroku login
# Add a remote to your local repository
heroku git:remote -a foodwebsite
# check that a remote named 'heroku' has been set for the app
git remote -v

git push heroku master
# to deploy from a branch besides master:
# git push heroku testbranch:master
```
