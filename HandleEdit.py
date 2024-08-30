import sqlite3
from handler import HandleRequests, status  # Import shared components
from views import get_tag_by_id, update_tag

# Handler class to handle tag editing
class EditTagHandler(HandleRequests):  # Inherit from HandleRequests

    # Method to display the edit form for a tag
    def edit_tag_view(self, tag_id):
        tag = get_tag_by_id(tag_id)
        if not tag:
            self.response('{"error": "Tag not found"}', status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
            return

        # Return tag data as JSON
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
