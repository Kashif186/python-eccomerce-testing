def test_get_post_by_id(api_client, base_url):
    response = api_client.get(f"{base_url}posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1