# Audio Server
 [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/deepgram/prompt/master/LICENSE)

1. POST raw audio data and store it. 

- $ curl -X POST --data-binary @myfile.wav http://localhost:8000/post 
- ($ curl -X POST -F file=@myfile.wav http://localhost:8000/post)

2. GET a list of stored files, GET the content of stored files, and GET metadata of stored files, such as the duration of the audio. The GET endpoint(s) should accept a query parameter that allows the user to filter results. Results should be returned as JSON. 

- $ curl --output test.wav http://localhost:8000/download?name=myfile.wav 

- $ curl http://localhost:8000/list?maxduration=300 

- $ curl http://localhost:8000/info?name=myfile.wav 

## Setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Run the server
```
./bin/run
```

## Run the tests
Unit tests in `tests/test_database.py'`
Integration tests:
```
./tests/bin/integration_test
```

## Structure
- `api.py` - defines the flask API endpoints
- `config.py` - defines flask configs
- `db/` - defines the peewee/sqlite database interface and query functions
- `tests/` - unit and integration tests


## Notes
- How to handle user authentication and data security?
  - Add the User model to the database and stored usernames and salted passwords.
  - Bind the user to the audio file and only allow the user to access their own files.
  - user have to log in to access the API, can use things like before_request in Flask to write check login function.
- How to build a simple browser UI to interface with your API?
  - Can use React or Vue as the front end to build a simple UI. 
  - Write a few HTML templates and use javascript to render the pages.
  - For current api, can have a sidebar of "upload" and "list" buttons, each corresponding to a different page.
    - For the upload page, can have a form that allows user to upload a file and submit.
    - For the list page, can have a table that shows the list of files and their metadata.
    - Each file in the list page has a download button besides it.
    - The list page can have a filter that allows user to filter the list by max duration.
- How do you want to store audio data? For the purposes of this interview, just keeping them in memory is fine, but how else would you want to keep and serve audio data?
  - For current scale, can store locally, renaming them with UUIDs.
  - For larger scale, can store in AWS S3 buckets.
  - If we are facing a global audience, can use AWS CDN, a distributed network of servers that can deliver content to users based on the geographic locations of the user.
  - To serve audio data, can use audio hosting sites like SoundCloud to store and serve audio data. Instead of storing a local path in the database, can now store a link to the file.
- How to handle data integrity? How to make sure that users can't break your API by uploading rogue text data? How to make sure the metadata you calculate is correct and not thrown off by unmet expectations on the backend? 
  - Can use TinyTag to parse the metadata of the audio file and check whether it is a valid audio file.
  - Can use an audio decoding library to thoroughly inspect the audio binary data and check whether it is broken.
    - Since the check may take some time, can use a background job queue like Celery to do the check.
    - Once the check is done, can inform the users whether the file is valid or not. The process is just like waiting for the check after uploading videos to Youtube.
  - Since we use libraries to parse the metadata and decode the audio data, we can trust the results. We don't need to calculate the metadata ourselves.
