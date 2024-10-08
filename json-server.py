import json
from http.server import HTTPServer
from handler import HandleRequests, status

from views import login_user, create_user, get_all_users, get_single_user
from views import get_all_tags, update_tag, delete_tag, create_tag
from views import get_categories, update_category, delete_category, create_category
from views import get_posts, get_single_post, update_post, delete_post, create_post, get_posts_by_user, update_post_approval
from views import get_all_comments, delete_comment, create_comment, update_comment, get_comments_by_post
from views import get_tags_by_post_id, add_tags_to_post, remove_tags_from_post, get_all_post_tags, delete_post_tag
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
                if "user_id" in url["query_params"]:
                    user_id = url["query_params"]["user_id"][0]
                    response_body = get_posts_by_user(user_id)
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)

                elif url["pk"] != 0:
                    response_body = get_single_post(url["pk"])
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)

                else:
                    response_body = get_posts()
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)

            elif url["requested_resource"] == "comments":
                response_body = get_all_comments()
                self.response(response_body, status.HTTP_200_SUCCESS.value)

            elif url["requested_resource"] == "users":
                if url["pk"] != 0:
                    response_body = get_single_user(url["pk"])
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)

                response_body = get_all_users()
                self.response(response_body, status.HTTP_200_SUCCESS.value)

            elif url["requested_resource"] == "posttags":
                # Check if a post_id is provided in the query parameters
                if "post_id" in url["query_params"]:
                    post_id = url["query_params"]["post_id"][0]
                    tags = get_tags_by_post_id(post_id)
                    response = json.dumps(tags)
                    self.response(response, status.HTTP_200_SUCCESS.value)
                else:
                    # If no post_id is provided, return all post-tag associations
                    post_tags = get_all_post_tags()
                    response = json.dumps(post_tags)
                    self.response(response, status.HTTP_200_SUCCESS.value)

            else:
                self.response(
                    json.dumps({"error": "Invalid resource"}),
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value
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
                post_data = self.rfile.read(content_length)
                user = json.loads(post_data)
                response = login_user(user)
                self.response(response, status.HTTP_200_SUCCESS.value)

            elif url["requested_resource"] == "register":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                user = json.loads(post_data)
                response = create_user(user)
                self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

            elif url["requested_resource"] == "categories":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                category = json.loads(post_data)
                new_category = create_category(category)
                if new_category:
                    self.response(json.dumps(new_category), status.HTTP_201_SUCCESS_CREATED.value)
                else:
                    self.response(
                        json.dumps({"error": "Failed to create category"}),
                        status.HTTP_500_SERVER_ERROR.value,
                    )

            elif url["requested_resource"] == "tags":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                tag = json.loads(post_data)
                new_tag = create_tag(tag)
                if new_tag:
                    self.response(json.dumps(new_tag), status.HTTP_201_SUCCESS_CREATED.value)
                else:
                    self.response(
                        json.dumps({"error": "Failed to create tag"}),
                        status.HTTP_500_SERVER_ERROR.value,
                    )
                    
            elif url["requested_resource"] == "posts":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                new_post = json.loads(post_data)
                created_post = create_post(new_post)
                if created_post:
                    self.response(json.dumps(created_post), status.HTTP_201_SUCCESS_CREATED.value)
                else:
                    self.response(
                        json.dumps({"error": "Failed to create post"}),
                        status.HTTP_500_SERVER_ERROR.value,
                    )

            if url["requested_resource"] == "posttags":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)

                post_id = data.get("post_id")
                tag_ids = data.get("tag_ids", [])

                if post_id and tag_ids:
                    success = add_tags_to_post(post_id, tag_ids)
                    if success:
                        self.response(
                            json.dumps({"message": "Tags successfully associated with post."}),
                            status.HTTP_201_SUCCESS_CREATED.value,
                        )
                    else:
                        self.response(
                            json.dumps({"error": "Failed to associate tags with post"}),
                            status.HTTP_500_SERVER_ERROR.value,
                        )
                else:
                    self.response(
                        json.dumps({"error": "Post ID and Tag IDs required"}),
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )
            
            elif url["requested_resource"] == "comments":
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                new_comment = json.loads(post_data)
                created_comment = create_comment(new_comment)
                if created_comment:
                    self.response(json.dumps(created_comment), status.HTTP_201_SUCCESS_CREATED.value)
                else:
                    self.response(
                        json.dumps({"error": "Failed to create comment"}),
                        status.HTTP_500_SERVER_ERROR.value,
                    )

            else:
                self.response(
                    json.dumps({"error": "Resource not found"}),
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        except Exception as e:
            print(f"Error processing POST request: {str(e)}")
            self.response(
                json.dumps({"error": "Internal server error"}),
                status.HTTP_500_SERVER_ERROR.value,
            )

    def do_PUT(self):
        try:
            url = self.parse_url(self.path)
            pk = url["pk"]

            content_len = int(self.headers["content-length"])
            request_body = self.rfile.read(content_len)
            request_body = json.loads(request_body)

            if url["requested_resource"] == "tags":
                tag_id = pk
                tag_data = request_body

                if pk != 0:
                    successfully_updated = update_tag(tag_id, tag_data["label"])
                    if successfully_updated:
                        return self.response(
                            {"message": "Tag updated successfully"},
                            status.HTTP_200_SUCCESS.value,
                        )
                    else:
                        return self.response(
                            {"message": "Tag not found"},
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )

            elif url["requested_resource"] == "posts":
                if pk != 0:
                    if "approved" in request_body:
                        approved = request_body["approved"]
                        successfully_updated = update_post_approval(pk, approved)
                    else:
                        successfully_updated = update_post(pk, request_body)

                    if successfully_updated:
                        return self.response(
                            {"message": "Post updated successfully"},
                            status.HTTP_200_SUCCESS.value,
                        )
                    else:
                        return self.response(
                            {"message": "Post not found"},
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )

            elif url["requested_resource"] == "categories":
                category_id = pk
                put_data = request_body

                if pk != 0:
                    successfully_updated = update_category(category_id, put_data)
                    if successfully_updated:
                        return self.response(
                            {"message": "Category updated successfully"},
                            status.HTTP_200_SUCCESS.value,
                        )
                    else:
                        return self.response(
                            {"message": "Category not found"},
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )

            elif url["requested_resource"] == "comments":
                if pk != 0:
                    successfully_updated = update_comment(pk, request_body)
                    if successfully_updated:
                        return self.response(
                            {"message": "Comment updated successfully"},
                            status.HTTP_200_SUCCESS.value,
                        )
                    else:
                        return self.response(
                            {"message": "Comment not found"},
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )

            # Handling the posttags update
            elif url["requested_resource"] == "posttags":
                post_id = request_body.get("post_id")
                new_tag_ids = request_body.get("tag_ids", [])

                if post_id is not None:
                    # Step 1: Remove all existing tags for this post
                    remove_success = remove_tags_from_post(post_id, [])

                    if remove_success:
                        # Step 2: If new_tag_ids is not empty, add the new tags to the post
                        if new_tag_ids:
                            success = add_tags_to_post(post_id, new_tag_ids)

                            if success:
                                return self.response(
                                    json.dumps({"message": "Post tags updated successfully"}),
                                    status.HTTP_200_SUCCESS.value,
                                )
                            else:
                                return self.response(
                                    json.dumps({"error": "Failed to update tags for post"}),
                                    status.HTTP_500_SERVER_ERROR.value,
                                )
                        else:
                            return self.response(
                                json.dumps({"message": "Tags removed, no new tags added"}),
                                status.HTTP_200_SUCCESS.value,
                            )
                    else:
                        return self.response(
                            json.dumps({"error": "Failed to remove existing tags for post"}),
                            status.HTTP_500_SERVER_ERROR.value,
                        )
                else:
                    return self.response(
                        json.dumps({"error": "Post ID and Tag IDs required"}),
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )

        except Exception as e:
            print(f"Error processing PUT request: {str(e)}")
            self.response(
                json.dumps({"error": "Internal server error"}),
                status.HTTP_500_SERVER_ERROR.value,
            )

    def do_DELETE(self):
        try:
            url = self.parse_url(self.path)
            pk = url["pk"]

            if url["requested_resource"] == "posts":
                if pk != 0:
                    successfully_deleted = delete_post(pk)
                    if successfully_deleted:
                        return self.response(
                            "Post deleted successfully", status.HTTP_200_SUCCESS.value
                        )
                    else:
                        return self.response(
                            "Post not found",
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )

            elif url["requested_resource"] == "categories":
                category_id = pk

                if pk != 0:
                    successfully_deleted = delete_category(category_id)
                    if successfully_deleted:
                        return self.response(
                            "Category deleted successfully",
                            status.HTTP_200_SUCCESS.value,
                        )
                    else:
                        return self.response(
                            "Category not found",
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )

            elif url["requested_resource"] == "tags":
                tag_id = pk

                if pk != 0:
                    successfully_deleted = delete_tag(tag_id)
                    if successfully_deleted:
                        return self.response(
                            "Tag deleted successfully",
                            status.HTTP_200_SUCCESS.value,
                        )
                    else:
                        return self.response(
                            "Tag not found",
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )

            elif url["requested_resource"] == "comments":
                if pk != 0:
                    successfully_deleted = delete_comment(pk)
                    if successfully_deleted:
                        return self.response(
                            "Comment deleted successfully",
                            status.HTTP_200_SUCCESS.value,
                        )
                    else:
                        return self.response(
                            "Comment not found",
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )

            elif url["requested_resource"] == "posttags":
                if pk != 0:
                    successfully_deleted = delete_post_tag(pk)  # Use function to delete by primary key
                    if successfully_deleted:
                        return self.response(
                            "Post tag association deleted successfully", 
                            status.HTTP_200_SUCCESS.value
                        )
                    else:
                        return self.response(
                            "Post tag association not found", 
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                        )

        except Exception as e:
            print(f"Error processing DELETE request: {str(e)}")
            self.response(
                json.dumps({"error": "Internal server error"}),
                status.HTTP_500_SERVER_ERROR.value,
            )

def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()