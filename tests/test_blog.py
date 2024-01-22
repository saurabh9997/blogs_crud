def test_create_blog_post(client, auth_token):
    # Test case: Create a new blogs post
    response = client.post('/api/blogs',
        json=dict(title='Test Blog Post', content='This is a test blogs post content.'),
        headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 201
    assert 'Blog post created successfully!' in str(response.json.get("message"))


def test_get_all_blog_posts(client):
    # Test case: Retrieve a list of all blogs posts
    response = client.get('/api/blogs')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_specific_blog_post(client, blog_post_id):
    # Test case: Retrieve details of a specific blogs post
    response = client.get(f'/api/blogs/{blog_post_id}')
    assert response.status_code == 200
    assert 'Test Blog Post' in str(response.json.get("title"))


def test_update_blog_post(client, auth_token, blog_post_id):
    # Test case: Update an existing blogs post
    response = client.put(f'/api/blogs/{blog_post_id}',
        json=dict(title='Updated Blog Post', content='This is the updated content of the blogs post.'),
        headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert 'Blog post updated successfully!' in str(response.json.get("message"))


def test_delete_blog_post(client, auth_token, blog_post_id):
    # Test case: Delete a blogs post
    response = client.delete(f'/api/blogs/{blog_post_id}', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert 'Blog post deleted successfully!' in str(response.json.get("message"))


def test_create_blog_post_unauthorized(client):
    # Test case: Attempt to create a new blogs post without authentication
    response = client.post('/api/blogs',
        json=dict(title='Unauthorized Post', content='This post should not be created without authentication.'))
    assert response.status_code == 401
    assert 'Missing Authorization Header' in str(response.data)


def test_update_blog_post_unauthorized(client, blog_post_id):
    # Test case: Attempt to update a blogs post without authentication
    response = client.put(f'/api/blogs/{blog_post_id}',
        json=dict(title='Unauthorized Update', content='This update should not be allowed without authentication.'))
    assert response.status_code == 401
    assert 'Missing Authorization Header' in str(response.data)


def test_delete_blog_post_unauthorized(client, blog_post_id):
    # Test case: Attempt to delete a blogs post without authentication
    response = client.delete(f'/api/blogs/{blog_post_id}')
    assert response.status_code == 401
    assert 'Missing Authorization Header' in str(response.data)
