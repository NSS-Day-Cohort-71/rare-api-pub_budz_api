import sqlite3
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from enum import Enum

# Status codes enum
class status(Enum):
    HTTP_200_SUCCESS = 200
    HTTP_201_SUCCESS_CREATED = 201
    HTTP_204_SUCCESS_NO_RESPONSE_BODY = 204
    HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA = 400
    HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND = 404
    HTTP_500_SERVER_ERROR = 500

# Main handler class
class HandleRequests(BaseHTTPRequestHandler):

    def response(self, body, code):
        self.set_response_code(code)
        self.wfile.write(body.encode())

    def parse_url(self, path):
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split("/")
        resource = path_params[1]

        url_dictionary = {"requested_resource": resource, "query_params": {}, "pk": 0}

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            url_dictionary["query_params"] = query

        try:
            pk = int(path_params[2])
            url_dictionary["pk"] = pk
        except (IndexError, ValueError):
            pass

        return url_dictionary

    def set_response_code(self, status):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    # Method to display the edit form for a tag
    def edit_tag_view(self, tag_id):
        tag = get_tag_by_id(tag_id)
        if not tag:
            self.response('{"error": "Tag not found"}', status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
            return

        # Return tag data as JSON (in practice, you might return HTML if it's rendered on the client)
        self.response(f"""
        {{
            "id": {tag["id"]},
            "label": "{tag["label"]}"
        }}
        """, status.HTTP_200_SUCCESS.value)

    # Method to handle tag editing submission
    def handle_edit_tag_submission(self, tag_id, form_data):
        new_label = form_data.get('label')
        if new_label:
            update_tag(tag_id, new_label)
            self.response('{"message": "Tag updated successfully"}', status.HTTP_200_SUCCESS.value)
        else:
            self.response('{"error": "Label is required"}', status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)


# Functions for database operations
def get_tag_by_id(tag_id):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id, label FROM Tags WHERE id = ?", (tag_id,))
    tag = cursor.fetchone()
    conn.close()
    if tag:
        return {"id": tag[0], "label": tag[1]}
    return None

def update_tag(tag_id, new_label):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("UPDATE Tags SET label = ? WHERE id = ?", (new_label, tag_id))
    conn.commit()
    conn.close()

# Request handler function
def handle_request(path, method, form_data=None):
    handler = HandleRequests()
    
    if path.startswith('/tags/edit/') and method == 'GET':
        tag_id = path.split('/')[-2]
        return handler.edit_tag_view(tag_id)
    elif path.startswith('/tags/edit/') and method == 'POST':
        tag_id = path.split('/')[-2]
        return handler.handle_edit_tag_submission(tag_id, form_data)
    # ... other routes
