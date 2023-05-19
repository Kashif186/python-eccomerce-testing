def test_delete_post(api_client, base_url):
    response = api_client.delete(f"{base_url}posts/1")
    assert response.status_code == 200
    assert response.text == "{}"