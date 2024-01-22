from flask import Blueprint, request

from app.blueprints.blogs.serializers import BlogPostSchema
from app.blueprints.blogs.service import create_or_update_blog, delete_blog_by_obj, get_blog_by_id, get_blogs
from app.middlewares.token import token_required
from app.utils.request_and_response_utils import get_pagination, make_json_response

blog_blueprint = Blueprint('blogs', __name__)
blog_post_schema = BlogPostSchema()


@blog_blueprint.route('/blogs', methods=['GET'])
def listing_blog():
    """
    Retrieve a list of all blogs posts.

    Returns:
        JSON response containing a list of blogs posts.
    """
    page_number = request.args.get("page")
    per_page = request.args.get("per_page")
    page_number, per_page = get_pagination(page_number, per_page)
    query = request.args.get("q", "")
    blog_posts = get_blogs(paginate=True,
        extra_params={"page_number": page_number, "per_page": per_page, "query": query})
    blog_list = blog_post_schema.dump(blog_posts, many=True)
    return make_json_response(blog_list, 201,
        {"page": page_number, "per_page": per_page, "total_pages": blog_posts.pages, })


@blog_blueprint.route('/blogs/<int:blog_id>', methods=['GET'])
def detailed_blog(blog_id):
    """
    Retrieve details of a specific blogs post.

    Args:
        blog_id (int): The ID of the blogs post to retrieve.

    Returns:
        JSON response containing the details of the specified blogs post.
    """
    blog = get_blog_by_id(blog_id)
    if not blog:
        return make_json_response({"error": 'Blog not found!'}, 404)

    blog_details = blog_post_schema.dump(blog)
    return make_json_response(blog_details, 201)


@blog_blueprint.route('/blogs', methods=['POST'])
@token_required
def create_blog(current_user):
    """
    Create a new blogs post.

    Args:
        current_user (User): The authenticated user creating the blogs post.

    Returns:
        JSON response indicating the success of the blogs creation.
    """
    data = request.get_json()
    errors = blog_post_schema.validate(data)
    if errors:
        return make_json_response({'error': 'Validation error', 'message': errors}, 400)

    data["current_user"] = current_user
    create_or_update_blog(data)
    return make_json_response({'message': 'Blog created successfully!'}, 200)


@blog_blueprint.route('/blogs/<int:blog_id>', methods=['PUT'])
@token_required
def update_blog(current_user, blog_id):
    """
    Update an existing blogs post.

    Args:
        current_user (User): The authenticated user updating the blogs post.
        blog_id (int): The ID of the blogs post to update.

    Returns:
        JSON response indicating the success of the blogs update.
    """
    blog = get_blog_by_id(blog_id)

    if not blog:
        return make_json_response({"error": 'Blog not found!'}, 404)

    if blog.author != current_user:
        return make_json_response({"error": 'Unauthorized!'}, 403)

    data = request.get_json()
    errors = blog_post_schema.validate(data)
    if errors:
        return make_json_response({'error': 'Validation error', 'message': errors}, 400)
    update_blog(blog, data)
    return make_json_response({'message': 'Blog updated successfully!'}, 200)


@blog_blueprint.route('/blogs/<int:blog_id>', methods=['DELETE'])
@token_required
def delete_blog(current_user, blog_id):
    """
    Delete an existing blogs post.

    Args:
        current_user (User): The authenticated user deleting the blogs post.
        blog_id (int): The ID of the blogs post to delete.

    Returns:
        JSON response indicating the success of the blogs deletion.
    """
    blog = get_blog_by_id(blog_id)

    if not blog:
        return make_json_response({"error": 'Blog not found!'}, 404)

    if blog.author != current_user:
        return make_json_response({"error": 'Unauthorized!'}, 403)

    delete_blog_by_obj(blog)
    return make_json_response({'message': 'Blog deleted successfully!'}, 204)
