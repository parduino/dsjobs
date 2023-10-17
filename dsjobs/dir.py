import os


def get_ds_directory_uri(cur_dir, ag):
    """
    Given the current directory on DesignSafe, determine the correct input URI.

    Args:
        ag (object): Agave object to fetch profiles or metadata.
        cur_dir (str): The current directory path.

    Returns:
        str: The corresponding input URI.
    """

    # If any of the following directory patterns are found in the current directory,
    # process them accordingly.
    directory_patterns = [
        ("jupyter/MyData", "designsafe.storage.default"),
        ("jupyter/mydata", "designsafe.storage.default"),
        ("jupyter/CommunityData", "designsafe.storage.community"),
    ]

    for pattern, storage in directory_patterns:
        if pattern in cur_dir:
            cur_dir = cur_dir.split(pattern).pop()
            input_dir = ag.profiles.get()["username"] + cur_dir
            input_uri = f"agave://{storage}/{input_dir}"
            return input_uri.replace(" ", "%20")

    project_patterns = [
        ("jupyter/MyProjects", "project-"),
        ("jupyter/projects", "project-"),
    ]

    for pattern, prefix in project_patterns:
        if pattern in cur_dir:
            cur_dir = cur_dir.split(pattern + "/").pop()
            project_id = cur_dir.split("/")[0]
            query = {"value.projectId": str(project_id)}
            cur_dir = cur_dir.split(project_id).pop()
            project_uuid = ag.meta.listMetadata(q=str(query))[0]["uuid"]
            input_uri = f"agave://{prefix}{project_uuid}{cur_dir}"
            return input_uri.replace(" ", "%20")

    return None
