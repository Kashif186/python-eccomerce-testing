def test_get_posts(api_client, base_url):
    response = api_client.get(f"{base_url}posts")
    assert response.status_code == 200
    assert len(response.json()) > 0