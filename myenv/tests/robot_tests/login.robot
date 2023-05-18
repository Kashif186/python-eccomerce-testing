*** Settings ***
Documentation    Login functionality
Resource          config.robot
Library           SeleniumLibrary

*** Test Cases ***
Successful Login
    [Setup]    Open Browser    ${BASE_URL}    ${BROWSER}    executable_path=${DRIVER_PATH}
    Input Text    id=user-name    ${USERNAME}
    Input Text    id=password    ${PASSWORD}
    Click Button    id=login-button
    Location Should Be    ${BASE_URL}/inventory.html
    [Teardown]    Close All Browsers
