import json
from http.server import HTTPServer
from handler import HandleRequests, status

from views import login_user, create_user


class JSONServer(HandleRequests):

    def do_GET(self):
        pass

    def do_POST(self):
        try:
            url = self.parse_url(self.path)

            if url["requested_resource"] == "login":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)  # Get the data sent by the client

                try:
                    user = json.loads(post_data)  # Parse the JSON data
                except json.JSONDecodeError:
                    return self.response(json.dumps({"error": "Invalid JSON"}), status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)

                response = login_user(user)  # Call the login function
                self.response(response, status.HTTP_200_SUCCESS.value)

            elif url["requested_resource"] == "register":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)  # Get the data sent by the client

                try:
                    user = json.loads(post_data)  # Parse the JSON data
                except json.JSONDecodeError:
                    return self.response(json.dumps({"error": "Invalid JSON"}), status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)

                response = create_user(user)  # Call the create_user function
                self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

            else:
                self.response(json.dumps({"error": "Resource not found"}), status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        except Exception as e:
            # Log the error and return a 500 status code
            print(f"Error processing POST request: {str(e)}")
            self.response(json.dumps({"error": "Internal server error"}), status.HTTP_500_SERVER_ERROR.value)

    def do_DELETE(self):
        pass

    def do_PUT(self):
        pass


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()

# 