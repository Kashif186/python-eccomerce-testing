*** Settings ***
Documentation    Logout functionality
Resource          config.robot
Resource          common_setup_teardown.robot
Library           SeleniumLibrary
Suite Setup       Common Setup
Suite Teardown    Common Teardown

*** Test Cases ***
Logout
    [Tags]    Logout
    Click Button    id=react-burger-menu-btn
    Wait Until Element is Visible    id=logout_sidebar_link
    Click Element    id=logout_sidebar_link
    Location Should Be    ${BASE_URL}/
