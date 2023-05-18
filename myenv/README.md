# python-eccomerce

Create, activate and deactivate environment:
python -m venv myenv
myenv\Scripts\activate

deactivate


Install dependencies inside the environment path

Install pytest:
pip install pytest

Install Requests for API Testing:
pip install requests

Install Selenium:
pip install selenium

Install Applitools Eyes for Visual Testing:
pip install eyes-selenium
pip install applitools-eyes-selenium

Install BDD:
pip install pytest-bdd

Install Robot Framework:
pip install robotframework
pip install robotframework-seleniumlibrary


Run tests in cmd:
pytest myenv/tests/selenium_tests/
behave myenv/tests/features/ 
robot myenv/tests/robot_tests/


