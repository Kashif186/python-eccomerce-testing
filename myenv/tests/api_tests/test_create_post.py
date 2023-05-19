def test_create_post(api_client, base_url):
    post_data = {
        "title": "Test Post",
        "body": "This is a test post.",
        "userId": 1
    }
    response = api_client.post(f"{base_url}posts", json=post_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"