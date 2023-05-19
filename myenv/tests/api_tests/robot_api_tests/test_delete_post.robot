*** Settings ***
Library           RequestsLibrary

*** Test Cases ***
Delete a Post
    Create Session  jsonplaceholder  https://jsonplaceholder.typicode.com
    ${response}     Delete Request  jsonplaceholder  /posts/1
    Should Be Equal As Strings  ${response.status_code}  200
