*** Settings ***
Documentation    Login functionality
Library           SeleniumLibrary

*** Variables ***
${BROWSER}    Chrome
${DRIVER_PATH}    ${CURDIR}/drivers/chromedriver
${BASE_URL}    https://www.saucedemo.com
${USERNAME}    standard_user
${PASSWORD}    secret_sauce
