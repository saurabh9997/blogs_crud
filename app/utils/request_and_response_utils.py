import json

from flask import current_app, make_response


def get_pagination(page_number, per_page):
    """
    Get valid pagination values from the provided parameters.

    Args:
        page_number (str or None): The requested page number.
        per_page (str or None): The requested items per page.

    Returns:
        Tuple[int, int]: A tuple containing valid page number and items per page.
    """
    if page_number and page_number.isdigit():
        page_number = int(page_number)
    else:
        page_number = 1
    page_number = page_number or 1
    max_per_page = current_app.config.get("MAX_PER_PAGE")
    if per_page and per_page.isdigit():
        per_page = int(per_page)
    else:
        per_page = max_per_page
    per_page = per_page if per_page and per_page <= max_per_page else max_per_page
    return page_number, per_page


def make_json_response(data, status_code, headers=None):
    """
    Create a JSON response with the provided data and status code.

    Args:
        data (dict): The data to be included in the JSON response.
        status_code (int): The HTTP status code for the response.
        headers (dict or None): Additional headers for the response.

    Returns:
        Response: The Flask response object containing JSON data.
    """
    if headers:
        return make_response(json.dumps(data, default=str), status_code, headers)
    return make_response(json.dumps(data, default=str), status_code)
