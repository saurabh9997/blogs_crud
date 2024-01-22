from sqlalchemy import or_

from app.blueprints.blogs.models.blog import BlogPost
from app.factories.application import db


def create_or_update_blog(data):
    """
    Create a new blog post if it does not exist, or update an existing one.

    Args:
        data (dict): Data containing blog post details.

    Returns:
        BlogPost: The created or updated blog post.
    """
    title = data.get('title')
    existing_blog = get_blog_by_title(title)
    if existing_blog:
        return update_blog(existing_blog, data)
    else:
        return create_blog(data)


def create_blog(data):
    """
    Create a new blog post.

    Args:
        data (dict): Data containing blog post details.

    Returns:
        BlogPost: The newly created blog post.
    """
    title = data.get('title')
    content = data.get('content')
    current_user = data.get("current_user")
    new_blog = BlogPost(title=title, content=content, author=current_user)
    db.session.add(new_blog)
    db.session.commit()
    return new_blog


def update_blog(existing_blog, data):
    """
    Update an existing blog post.

    Args:
        existing_blog (BlogPost): The existing blog post to be updated.
        data (dict): Data containing updated blog post details.

    Returns:
        bool: True if the update is successful.
    """
    existing_blog.content = data.get('content', existing_blog.content)
    existing_blog.author = data.get('author', existing_blog.author)
    db.session.commit()
    return True


def get_blog_by_id(id):
    """
    Retrieve a blog post by its ID.

    Args:
        id (int): The ID of the blog post.

    Returns:
        BlogPost: The blog post with the specified ID.
    """
    return BlogPost.query.get(id)


def get_blog_by_title(title):
    """
    Retrieve a blog post by its title.

    Args:
        title (str): The title of the blog post.

    Returns:
        BlogPost: The blog post with the specified title.
    """
    return BlogPost.query.filter_by(title=title).first()


def get_blogs(paginate=False, extra_params=None):
    """
    Retrieve a list of blog posts with optional pagination and filtering.

    Args:
        paginate (bool): Whether to paginate the results.
        extra_params (dict): Additional parameters including page_number, per_page, and query.

    Returns:
        List[BlogPost] or Pagination: List of blog posts or paginated blog posts.
    """
    extra_params = extra_params or {}
    page_number = extra_params.get("page_number")
    per_page = extra_params.get("per_page")
    query = extra_params.get("query")
    base_query = BlogPost.query

    if not paginate:
        return base_query.all()
    if page_number and per_page and query:
        base_query = base_query.filter(or_(BlogPost.title.ilike(f'%{query}%'), BlogPost.content.ilike(f'%{query}%')))
    return base_query.paginate(page=page_number, per_page=per_page)


def delete_blog_by_obj(blog):
    """
    Delete a blog post.

    Args:
        blog (BlogPost): The blog post to be deleted.

    Returns:
        bool: True if the deletion is successful.
    """
    db.session.delete(blog)
    db.session.commit()
    return True
