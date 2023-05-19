def test_update_post(api_client, base_url):
    post_data = {
        "title": "Updated Post",
        "body": "This post has been updated."
    }
    response = api_client.put(f"{base_url}posts/1", json=post_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Post"