
#Update server packages

sudo apt-get update
sudo apt-get install

#install packages

run scripts/install_packages.sh to install additional packages

#generate keys for github

ssh-keygen -t rsa -C "craig@hacklaunch.com"
Update your git hub keys


#Clone the repo

git clone git@github.com:NgJaime/HackLaunch.git


#Create virtual environment

cd HackLaunch
virtualenv -p python venv
source evnv/bin/activate


#Install requirements

pip install -r requirements/production.txt


#Configuration

*hacklaunch/settings/production.py
	**Update allowed hosts
	**Update databse connection

*nginx
	**cp /home/ubuntu/HackLaunch/config/nginx/nginx.conf /etc/nginx/nginx.conf

*supervisor
	**cp /home/ubuntu/HackLaunch/config/supervisor/production-hacklaunch.conf /etc/supervisor/conf.d/production-hacklaunch.conf
	**cp /home/ubuntu/HackLaunch/config/supervisor/supervisord.conf /etc/supervisor/supervisord.conf



#keys.py
Add the file hacklaunch/settings/keys.py

It should contain:
*the django secret key
*social auth identies
*email settings
vasw keys
*database user, password and host


#SSL connection to db
Download the public key stored at http://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem to ~/.ssh/rds-combined-ca-bundle.pem


#Server SSL connections

/home/ubuntu/HackLaunch/config/keys/staging.hacklaunch.com_combined.crt

[If you need a new ssl keys]

cd /etc/ssl/certs && openssl dhparam -out dhparam.pem 2048
mkdir /etc/nginx/ssl
cp /etc/ssl/certs/dhparam.pem /etc/nginx/ssl/dhparam.pem

openssl req -new -newkey rsa:2048 -nodes -keyout production.hacklaunch.key -out production.hacklaunch.csr

Country Name (2 letter code) [AU]:SG
State or Province Name (full name) [Some-State]:Singapore
Locality Name (eg, city) []:Singapore
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Hacklaunch
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:www.hacklaunch.com
Email Address []:webmaster@hacklaunch.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:

*upload the csr to godaddy to generate the key set. 
*once ready downlaod the keys
*copy to the server scp -i ~/.ssh/hacklaunch-staging.pem * ubuntu@xxx.xxx.xxx.xxx:/home/ubuntu/HackLaunch/config/keys
*on the server combine the keys provide by godaddy
	cat 8f0725f4c84fa468.crt gd_bundle-g2-g1.crt > hacklaunch.combined.crt


#Starting services
service supervisor start
sudo supervisorctl update
sudo supervisorctl start hacklaunch

sudo service nginx start


#Notes
Make sure the database VPC allows connections from your server's IP

To check nginx conf: nginx -t -c /etc/nginx/nginx.conf
