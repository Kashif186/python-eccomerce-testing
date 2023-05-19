*** Settings ***
Library           RequestsLibrary

*** Test Cases ***
Update an Existing Post
    Create Session  jsonplaceholder  https://jsonplaceholder.typicode.com
    ${headers}=     Create Dictionary  Content-Type=application/json
    ${payload}=     Create Dictionary  id=1  title=Updated Post  body=Hello, updated world!
    ${response}     Put Request  jsonplaceholder  /posts/1  headers=${headers}  json=${payload}
    Should Be Equal As Strings  ${response.status_code}  200
