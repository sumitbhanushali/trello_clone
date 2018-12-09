## APIs of Trello Clone developed in django and django rest framework for learning purposes
----

to install dependencies

    pip3 install -r requirements.txt 

to start server:

    python3 manage.py runserver

   

----
## APIS
> POST auth/login
   
    {
        "username": "test",
        "password": "testpassword"
    }

> POST auth/logout
 
    {

    }

> POST auth/registration/

    {
        "username": "test",
        "email": "email@email.com",
        "password": "testpassword"
    }

> PUT trello-users/

    {
        "id": 1
        "IsPremium": True
    }

> POST boards/

    {
        "Name": "board1"
    }


> GET board-members/


*fetch loggedin user's boards*


> GET lists?BoardID=1

*fetch all lists and respective cards with attachments of selected Board*

> POST lists/

    {
        "Name": "list1",
        "BoardID": 1
    }

 > POST cards/

    {
        "Name": "card1",
        "Description": "card_description",
        "ListID": 1,
        "pos": 1
    }

> PUT cards/

    {
        "id": 1,
        "DueDate": "2018-12-22T22:10:19"
    }

> GET card/1

*fetch card details*

> POST attachments/

    {
        "CardID": 1,
        "Url": "http://xyz.com"
    }
    
----
## next steps
* develop frontend in react
* dockerize

