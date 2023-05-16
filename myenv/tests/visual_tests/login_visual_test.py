def test_login_visual(driver, login, eyes):
    with eyes.open(driver, "Ecommerce App", "Login Page") as eyes_session:
        eyes_session.check_window("Logged in")
