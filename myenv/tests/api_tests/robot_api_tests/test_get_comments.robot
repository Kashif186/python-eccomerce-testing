*** Settings ***
Library           RequestsLibrary

*** Test Cases ***
Get Comments for a Post
    Create Session  jsonplaceholder  https://jsonplaceholder.typicode.com
    ${response}     Get Request  jsonplaceholder  /comments?postId=1
    Should Be Equal As Strings  ${response.status_code}  200
