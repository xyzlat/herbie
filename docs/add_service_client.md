##### 1) Create super user
```
python manage.py createsuperuser --username "username" --email "email-address"
```
##### 2) Log in the admin panel as super user  
```
http://localhost:8000/admin
```
##### 3) Create user with username, the name of the service

##### 4) Go to Users in the admin panel and choose your new user-service

##### 5) Go to the permissions section and add groups
```
Each group represent a business entity channel/topic.
You can define which business entities your service is authorized 
to publish data
```
##### 5) Create a token for your new user-service
```
Go to Tokens -> add Token -> choose your new user-service -> save
```