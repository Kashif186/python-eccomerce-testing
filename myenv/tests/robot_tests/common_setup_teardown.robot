*** Settings ***
Library    SeleniumLibrary
Resource          config.robot

*** Keywords ***
Common Setup
    [Documentation]    Common setup steps
    Open Browser    ${BASE_URL}    ${BROWSER}    executable_path=${DRIVER_PATH}
    Input Text    id=user-name    ${USERNAME}
    Input Text    id=password    ${PASSWORD}
    Click Button    id=login-button

Common Teardown
    [Documentation]    Common teardown steps
    Close All Browsers

