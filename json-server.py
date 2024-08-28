import json
from http.server import HTTPServer
from handler import HandleRequests, status

from views import login_user, create_user
from views import get_all_tags  # Import the function to fetch tags
from views import get_categories
from views import get_posts
from views import update_tag, get_tag_by_id  # Import the necessary functions


class JSONServer(HandleRequests):

    def do_GET(self):
        try:
            url = self.parse_url(self.path)

            if url["requested_resource"] == "tags":
                tags = get_all_tags()
                response = json.dumps(tags)
                self.response(response, status.HTTP_200_SUCCESS.value)
            elif url["requested_resource"] == "categories":
                response_body = get_categories()
                self.response(response_body, status.HTTP_200_SUCCESS.value)
            elif url["requested_resource"] == "posts":
                response_body = get_posts()
                self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                self.response(
                    "Resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        except Exception as e:
            print(f"Error processing GET request: {str(e)}")
            self.response(
                json.dumps({"error": "Internal server error"}),
                status.HTTP_500_SERVER_ERROR.value,
            )

    def do_POST(self):
        try:
            url = self.parse_url(self.path)

            if url["requested_resource"] == "login":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(
                    content_length
                )  # Get the data sent by the client

                try:
                    user = json.loads(post_data)  # Parse the JSON data
                except json.JSONDecodeError:
                    return self.response(
                        json.dumps({"error": "Invalid JSON"}),
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )

                response = login_user(user)  # Call the login function
                self.response(response, status.HTTP_200_SUCCESS.value)

            elif url["requested_resource"] == "register":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(
                    content_length
                )  # Get the data sent by the client

                try:
                    user = json.loads(post_data)  # Parse the JSON data
                except json.JSONDecodeError:
                    return self.response(
                        json.dumps({"error": "Invalid JSON"}),
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )

                response = create_user(user)  # Call the create_user function
                self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

            else:
                self.response(
                    json.dumps({"error": "Resource not found"}),
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        except Exception as e:
            # Log the error and return a 500 status code
            print(f"Error processing POST request: {str(e)}")
            self.response(
                json.dumps({"error": "Internal server error"}),
                status.HTTP_500_SERVER_ERROR.value,
            )

    def do_DELETE(self):
        pass

    def do_PUT(self):
        try:
            url = self.parse_url(self.path)

            if url["requested_resource"] == "tags":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)  # Get the data sent by the client

                try:
                    tag_data = json.loads(post_data)  # Parse the JSON data
                except json.JSONDecodeError:
                    return self.response(json.dumps({"error": "Invalid JSON"}), status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)

                tag_id = url["pk"]
                existing_tag = get_tag_by_id(tag_id)  # Ensure the tag exists

                if not existing_tag:
                    return self.response(json.dumps({"error": "Tag not found"}), status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

                # Update the tag in the database
                update_tag(tag_id, tag_data['label'])
                self.response(json.dumps({"message": "Tag updated successfully"}), status.HTTP_200_SUCCESS.value)
            else:
                self.response(json.dumps({"error": "Resource not found"}), status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        except Exception as e:
            # Log the error and return a 500 status code
            print(f"Error processing PUT request: {str(e)}")
            self.response(json.dumps({"error": "Internal server error"}), status.HTTP_500_SERVER_ERROR.value)


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()

#
