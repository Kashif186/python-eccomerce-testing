*** Settings ***
Library           RequestsLibrary

*** Test Cases ***
Create a New Post
    Create Session  jsonplaceholder  https://jsonplaceholder.typicode.com
    ${headers}=     Create Dictionary  Content-Type=application/json
    ${payload}=     Create Dictionary  title=New Post  body=Hello, world!  userId=1
    ${response}     Post Request  jsonplaceholder  /posts  headers=${headers}  json=${payload}
    Should Be Equal As Strings  ${response.status_code}  201
