# David-Learns-Django

The following project is a project I took up to learn Django by following a video by PyPlane at the following link - https://www.youtube.com/watch?v=04L0BbAcCpQ! The project revolves around creating a web application that ...

## Libraries used

The following libraries were used in the project:

- Django / Django-Crispy-Forms
- Matplotlib
- Seaborn
- Pandas
- XHtml2Pdf

## Setting up

A project is first created using 'django-admin startproject {projectName}'  
Then, a Sqlite3 database was created using 'python manage.py migrate'  
Then, a super user was created using 'python manage.py createsuperuser'  
Then, 'python manage.py runserver' was used to start the development server  
Then, a templates folder was added to src after changing template directory in settings.py  
Then, we ended by adding the 'static' and 'media' directories are required

### Applications

The following applications were then started with 'python manage.py startapp {name}':

- Sales
- Reports
- Profiles
- Products
- Customers

Do remember to add these applications along with crispy_forms to 'settings.py'

## Concepts Covered

The concepts covered in the project includes:

- Models / Views / Templates
- Signals
- Forms
- URLs
- Dropzone

## Running the application

Use 'python manage.py runserver' to start the application

## Snapshots

The home page shown below allows the user to filter transactions based on the date_from and date_to as well as choose how to filter the transactions and the type of chart required!
![Market](/snapshots/Home.PNG)

The web app has a authentication system!
![Market](/snapshots/Authentication.PNG)

The details of transactions can be shown in the page below! Reports can also be generated in the PDF format!
![Market](/snapshots/Details.PNG)
![Market](/snapshots/Reports.PNG)

CSV data can be uploaded via a dropzone and the various objects will be created automatically!
![Market](/snapshots/Uploading.PNG)

Users can customize their profiles!
![Market](/snapshots/Profile.PNG)
