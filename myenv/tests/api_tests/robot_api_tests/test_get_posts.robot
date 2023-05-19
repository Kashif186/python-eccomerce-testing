*** Settings ***
*** Settings ***
Library           RequestsLibrary

*** Test Cases ***
Get All Posts
    Create Session  jsonplaceholder  https://jsonplaceholder.typicode.com
    ${response}     Get Request  jsonplaceholder  /posts
    Should Be Equal As Strings  ${response.status_code}  200
