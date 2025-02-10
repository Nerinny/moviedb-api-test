# API tests for Movie DB endpoints
API tests of get top rated movies and rate movie endpoints. Done with Python, Pytest and Requests. Includes Dockerfile and GH actions pipeline with HTML report.
Performance basic tests in Locust in separate jobs in GH pipeline with csv report.
## Running solution in GH
- GH Actions pipeline is available in Actions tab of repository, it runs docker container and generates HTML report which is available in run artifacts. Bearer token is saved as GH secret.
- GH Actions pipeline has separate jobs for locust performance tests. They run in three modes for a minute and each produces csv results attached to run artifacts. Locust tests reuse helper fucntions and again bearer token is saved as GH secret.
## Running solution locally
- Clone repository locally
- Generate bearer token for your [Movie DB developer](https://developer.themoviedb.org/)
- Build docker image:
```docker build . --file Dockerfile --tag moviedb-api-test:latest```
- Run docker and set variable `BEARER_TOKEN`:
```docker run --rm -e BEARER_TOKEN=<your_bearer_token_here> moviedb-api-test:latest```
- Run performance tests with the same `BEARER_TOKEN` as local env variable. You can specify one of performance scenarios (burst, staggered, normal) as a scenario argument.
```locust -f performance/locustfile.py --scenario=burst --headless --run-time 1m --only-summary --csv=locust/locust_log```
## Structure of solution
- **.github/workflows/docker-image.yml** - GH workflow configuration
- **config.ini** - configuration file with endpoints
- **Dockerfile** - commands to create docker container
- **pytest.ini** - configuration of pytest
- **requirements.txt** - required libraries
- **helpers/request_helper.py** - helper methods that make requests to endpoint and have already set default values
- **testdata/messages.py** - endpoints response messages for assertions
- **testdata/response_schema** - schemas for responses for assertions
- **tests/test_add_rating_endpoint** - tests for add movie rating endpoint
- **tests/test_top_rated_endpoint** - tests for top rated movies endpoint
- **perfrormance/locustfile.py** - performance tests for top rated movies endpoint

## Test scenarios
### Feature: Add rating endpoint
Scenario: Check access status codes
1. GIVEN user has valid bearer token  
WHEN user sends request to add rating  
THEN endpoint returns response 201 
  

2. GIVEN user has invalid bearer token  
WHEN user sends request to add rating  
THEN endpoint return response 401  
  

3. GIVEN user doesn't specify bearer token  
WHEN user sends request to add rating  
THEN endpoint returns response 401

Scenario: Check invalid rating responses  
  
4. GIVEN user sets rating as 0  
WHEN user sends request to add rating  
THEN endpoint returns response 400  
AND status message about rating being too low  


5. GIVEN user sets rating as a string  
WHEN user sends request to add rating  
THEN endpoint returns response 400  
AND status message about rating being too low  
  

6. GIVEN user sets rating as 100000  
WHEN user sends request to add rating  
THEN endpoint returns response 400  
AND status message about rating being too high

Scenario: Check sending request with wrong parameters  
  
7. GIVEN user sets wrong parameters  
WHEN user sends request to add rating  
THEN endpoint returns response 400  
AND status message about invalid parameters  

Scenario: Check updating rating of a movie  
  
8. GIVEN user already rated the movie  
WHEN user sends request to add rating to the same movie  
THEN endpoint returns response 201  
AND status message about successful update  

Scenario: Check rating movie that doesn't exist in db  

9. GIVEN user sets ID of movie that doesn't exist in db  
WHEN user sends request to add rating  
THEN endpoint returns response 404  
AND status message about resource not found

Scenario: Check rating movie with wrong ID

10. GIVEN user sets ID of movie as 0  
WHEN user sends request to add rating  
THEN endpoint returns response 404  
AND status message about invalid ID  
  

11. GIVEN user sets ID of movie as -1  
WHEN user sends request to add rating  
THEN endpoint returns response 404  
AND status message about invalid ID
  

12. GIVEN user sets ID of movie as a string  
WHEN user sends request to add rating  
THEN endpoint returns response 404  
AND status message about invalid ID

Scenario: Check schema of response of rating movie

13. GIVEN user sets proper parameters  
WHEN user sends request to add rating  
THEN endpoint returns response that fits specified schema

### Feature: Get top rated movies endpoint
Scenario: Check access status codes

1. GIVEN user has valid bearer token  
WHEN user sends request to get top movies   
THEN endpoint returns response 201 
  

2. GIVEN user has invalid bearer token  
WHEN user sends request to get top movies   
THEN endpoint return response 401  
  

3. GIVEN user doesn't specify bearer token  
WHEN user sends request to get top movies     
THEN endpoint returns response 401

Scenario: Check defaulting to english language

4. GIVEN user sets invalid language in parameter
WHEN user sends request to get top movies    
THEN endpoint returns response 200  
AND movie title in response is in english  
AND movie overview in response is in english

Scenario: Check different language parameter

5. GIVEN user sets Polish language in parameter
WHEN user sends request to get top movies     
THEN endpoint returns response 200  
AND movie overview in response is in Polish
  
  
6. GIVEN user sets English language in parameter
WHEN user sends request to get top movies     
THEN endpoint returns response 200    
AND movie overview in response is in English
  

7. GIVEN user sets Dutch language in parameter
WHEN user sends request to get top movies     
THEN endpoint returns response 200  
AND movie overview in response is in Dutch

Scenario: Check non existent API endpoint

8. GIVEN user has wrong endpoint url  
WHEN user sends request     
THEN endpoint returns response 404

Scenario: Check omitting required parameters

9. GIVEN user omits required parameters  
WHEN user sends request to get top movies     
THEN endpoint returns response 400 or 401

Scenario: Check pagination

10. GIVEN user sets page parameter to 1  
WHEN user sends request to get top movies     
THEN endpoint returns response 200  
AND page number in response is 1  
AND number of total pages in response in more than 1  
  
  
11. GIVEN user sets page parameter to 50  
WHEN user sends request to get top movies    
THEN endpoint returns response 200  
AND page number in response is 50  
AND number of total pages in response in more than 1  
  
  
12. GIVEN user sets page parameter to 100  
WHEN user sends request to get top movies    
THEN endpoint returns response 200  
AND page number in response is 100  
AND number of total pages in response in more than 1  

Scenario: Check invalid page parameter

13. GIVEN user sets page parameter to 0  
WHEN user sends request to get top movies     
THEN endpoint returns response 400
AND status message about invalid page number  
  
  
14. GIVEN user sets page parameter to a string  
WHEN user sends request to get top movies     
THEN endpoint returns response 400
AND status message about invalid page number

  
15. GIVEN user sets page parameter to 100000
WHEN user sends request to get top movies     
THEN endpoint returns response 400
AND status message about invalid page number

Scenario: Check schema of response of getting top movies

16. GIVEN user sets proper parameters  
WHEN user sends request to get top movies   
THEN endpoint returns response that fits specified schema


