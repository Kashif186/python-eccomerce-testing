import pytest
from applitools.selenium import Eyes

@pytest.fixture(scope='function')
def eyes():
    # Set up Applitools Eyes instance
    eyes = Eyes()
    # Set your Applitools API key here
    eyes.api_key = 'SWNqhp6104CsVaaojjoR5Zhj54pu6zTLv3SsxqxSR1C18110'
    yield eyes
    # Close the Applitools Eyes session
    eyes.close()