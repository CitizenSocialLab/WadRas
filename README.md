# README #

## CitizenSocialLab: WadRas ##

Experiment designed and implemented to be performed in **WadRas** during the performance [Veus entre Murs](http://escenapoblenou.com/activitats/veus-entre-murs/).

This participatory experiment consist on a set of dilemmas presented as behavioural games, **four Prisoner's Dilemma**, designed to relate participants: (1) random selection, (2) staring eyes, (3) wall in-out, and (4) wall out-in. The selections 3 and 4 are asyncron. All these games are played by 2 individuals.

## Data ##
**Not available**  

## Derived Scientific Publications ##
**Not available**

## Configuration ##
Steps are necessary to get WADRAS install, up and running in local network.

### Creation of the project ###

__Database MySQL__  
Create MySQL database: name\_db  
Create user database: user\_db  
Create password database: pass\_db  

Introduce this information about the database in: `/WadRas/settings.py`

__Environment__  
```mkvirtualenv wadras```

__Requirements__  
```pip install -r requirements.txt```

__MongoDB__  
```mongod --dbpath /.../wadras/ddbb```

__Load text__ 
File with text and translations:  `/.../WadRas/game/i18n/translations.xlsx`  

```python excel\_to\_mongodb.py```

__Run Server__  
```python manage.py runserver```
```python manage.py runserver localhost:port```

__Migrations__  
```python manage.py makemigrations```  
```python manage.py migrate```

### Run project in Local ###

__Step 1: Run MySQL server__  
Run MySQL: `mysql.server start`

__Step 2: Open terminal tabs and work on the environment__  

in Tab 1: MongoDB  
in Tab 2: MySQL  
in Tab 3: Run Application  

Work on environment (in each terminal tab): `workon wadras`

__Step 3: Run MongoDB (Tab 1)__  
Run mongodb: `mongod --dbpath /.../WadRas/ddbb`

__Step 4: MySQL actions (Tab 2)__  
Directory: `cd /.../WadRas/`   
Database: `mysql -u user_db -p (pass_db)`

Drop database: `drop database name\_db;`  
Create database: `create database name\_db;`  
Exit: `exit;`

Modificate fields of database: `python manage.py makemigrations`  
Refresh database:
`python manage.py migrate` 

__Step 5: Load texts (Tab 2)__    
Load translations: `python excel_to_mongodb.py`

__Step 6: Load actions "Wall in-out" (Tab 2)__    
Load actions: `python wadras_prisoners.py`

__Step 7: Run Server (Tab 3)__  
Directory: `cd /.../WadRas/ `   
Runserver: `python manage.py runserver localhost:port`

### Access client ###
Client application:  
**http://localhost:port/**  
 
Control and Administration:  
**http://localhost:port/admin**
## Versions ##
Version 1.0

## License ##
CitizenSocialLab | WadRas (c) by Julian Vicens

CitizenSocialLab | WadRas is licensed under a
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see [CC BY-NC-SA license](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Contact ##

Julian Vicens: **julianvicens@gmail.com**
