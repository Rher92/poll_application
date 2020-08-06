# Poll app

This mini-app is an API to create Polls.

## How to run the platform ##

run the app on space of your preferences, you must follow the next steps:

Step one:
  in this steps you must download the repo code. 
  
  * git clone https://github.com/Rher92/poll-application.git

Step two:
  you must move to poll_application folder, where the repository is located.
  
  * cd poll_application
  
Step three:
  now, you have to create the docker container.
  
  * docker-compose up --build
  
  
## How to use the API ##

Next examples, we will use the Python Requests Library to help us to make the requests.

the **username** param on url belong to your account.
the **token** param on url belong to your account.

**how to create an user**
  
  - username = 'Pepito'
  - password = '123456'
  - email = 'pepito@gamil.com'
  - url = 'http://127.0.0.1:8000/api/auth/signup'
  - data = {'username': username, 'email': 'pepito@gmail.com', 'password':password}
  - r = requests.post(url, data = data)


**how to get a token to make requests**

  - url='http://127.0.0.1:8000/api/auth/generate_token'
  - auth=(username, password)
  - r = requests.put(url, auth=auth)
  - token = r.json().put('token')


**how to create a poll**

  - url='http://127.0.0.1:8000/api/poll/new/users/{}/token/{}'.format(username, token)
  - data={'title': 'First Poll', \
  'questions': ['First question', 'Second question'], \
  'tags': ['First tag', 'Second tag'], \
  'close_date': '2020-11-04 00:05:23'}
  - r = requests.post(url, data = data)


**how to get questions of all polls**

  - to get all questions of the all users:
      - url='http://127.0.0.1:8000/api/poll/questions/users/{}/token/{}'.format(username, token)
      - params = {'user': 'all'}
      - r = requests.get(url, params=params)

  - to get questions of an specific user:
      - url='http://127.0.0.1:8000/api/poll/questions/users/{}/token/{}'.format(username, token)
      - params = {'user': 'Pepito'}
      - r = requests.get(url, params=params)

  - Response:
    - {'users': 
        [{'pepito': 
          {'polls': 
            [{'id': 1, 'questions': [{'id': 1, 'title': 'First question'}, 
             {'id': 2, 'title': 'Second question'}], 'title': 'First poll'}]
           }
         }]
      }


**how to response a questions**

  the **id_poll** params is the id belong the poll.
  the **id_question** is the id belong to question.

  - url='http://127.0.0.1:8000/api/poll/{}/answer'.format(id_poll)
  - data={'**id_question**': 'answer1', '**id_question**': 'answer2'}
  - r = requests.post(url, data=data)


**how to get a list of all the polls**

  - url='http://127.0.0.1:8000/api/poll/all/users/{}/token/{}'.format(username, token)
  - r = requests.get(url)
  
  - Response:
    - {'poll': [{'id': 1, 'title': 'First poll'}]}
  
  
**how to get a list of all polls through a tag**

  - url='http://127.0.0.1:8000/api/poll/all/users/{}/token/{}'.format(username, token)
  - params = {'tag': 'First tag'}
  - r = requests.get(url, params=params)
  
  - Response 
    - {'poll': [{'id': 1, 'title': 'First poll'}]}
  
  
**how to return full data to one user**
 
  - url='http://127.0.0.1:8000/api/poll/questions_and_answers/users/{}/token/{}'.format(username, token)
  - params = {'user': 'Pepito'}
  - r = requests.get(url, params=params)  
  
  - Response:
       - {'data': 
            [{'polls': 
                [{'id': 1, 
                'questions': 
                    [{'answers': 
                        [{'answer': 'answer1', 'id': 1}, 
                        {'answer': 'answer1', 'id': 3}, 
                        {'answer': 'answer1', 'id': 5}, 
                        {'answer': 'answer1', 'id': 7}], 
                    'id': 1, 
                    'title': 'First question'}, 
                    {'answers': 
                        [{'answer': 'answer2', 'id': 2}, 
                        {'answer': 'answer2', 'id': 4}, 
                        {'answer': 'answer2', 'id': 6}, 
                        {'answer': 'answer2', 'id': 8}], 
                    'id': 2, 
                    'title': 'Second question'}], 
                'title': 'First poll'}]}], 
        'user': 'pepito'}

