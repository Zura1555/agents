"""
ClickUp API Client

Provides comprehensive API access to ClickUp for managing tasks, lists,
folders, spaces, and time tracking.

Author: Thuong-Tuan Tran
Version: 1.0.0
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin


class ClickUpAPIError(Exception):
    """Custom exception for ClickUp API errors."""
    pass


class ClickUpAPIClient:
    """
    ClickUp API client with authentication, rate limiting, and error handling.

    Supports:
    - Tasks CRUD operations
    - Lists management
    - Folders and Spaces
    - Time tracking
    - Teams and Users
    - Webhooks
    """

    def __init__(self, api_token: str, base_url: str = "https://api.clickup.com"):
        """
        Initialize ClickUp API client.

        Args:
            api_token: ClickUp API token
            base_url: Base URL for ClickUp API (default: production)
        """
        self.api_token = api_token
        self.base_url = base_url
        self.session = self._create_session()
        self.rate_limit_remaining = 100
        self.rate_limit_reset = 0

    def _create_session(self):
        """Create authenticated requests session."""
        import requests

        session = requests.Session()
        session.headers.update({
            "Authorization": f"{self.api_token}",
            "Content-Type": "application/json"
        })
        return session

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Make HTTP request to ClickUp API with rate limiting and retries.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint (e.g., '/api/v2/team')
            data: Request body data
            params: URL parameters
            retry_count: Current retry attempt

        Returns:
            API response as dictionary

        Raises:
            ClickUpAPIError: On API errors
        """
        # Rate limiting
        current_time = int(time.time())
        if current_time < self.rate_limit_reset:
            sleep_time = self.rate_limit_reset - current_time
            print(f"Rate limit reached. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)

        # Build URL
        url = urljoin(self.base_url, endpoint.lstrip("/"))

        # Make request
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params
            )

            # Update rate limit info
            if 'X-RateLimit-Remaining' in response.headers:
                self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
            if 'X-RateLimit-Reset' in response.headers:
                self.rate_limit_reset = int(response.headers['X-RateLimit-Reset'])

            # Handle response
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 201:
                return response.json()
            elif response.status_code == 429:
                # Rate limited - retry with backoff
                if retry_count < 3:
                    retry_delay = (2 ** retry_count) * 5
                    print(f"Rate limited. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    return self._make_request(
                        method, endpoint, data, params, retry_count + 1
                    )
                else:
                    raise ClickUpAPIError("Max retries reached for rate limiting")
            elif response.status_code == 401:
                raise ClickUpAPIError("Authentication failed. Check API token.")
            elif response.status_code == 403:
                raise ClickUpAPIError("Forbidden. Check permissions.")
            elif response.status_code == 404:
                raise ClickUpAPIError(f"Resource not found: {endpoint}")
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                raise ClickUpAPIError(error_msg)

        except requests.exceptions.RequestException as e:
            if retry_count < 3:
                retry_delay = (2 ** retry_count) * 5
                print(f"Request failed: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                return self._make_request(
                    method, endpoint, data, params, retry_count + 1
                )
            else:
                raise ClickUpAPIError(f"Request failed after 3 retries: {e}")

    # ========================================
    # Teams and Users
    # ========================================

    def get_teams(self) -> Dict[str, Any]:
        """
        Get all teams accessible by the user.

        Returns:
            Dictionary with teams list
        """
        return self._make_request("GET", "/api/v2/team")

    def get_team(self, team_id: str) -> Dict[str, Any]:
        """
        Get a specific team by ID.

        Args:
            team_id: Team ID

        Returns:
            Team data
        """
        return self._make_request("GET", f"/api/v2/team/{team_id}")

    def get_users(self, team_id: str) -> Dict[str, Any]:
        """
        Get all users in a team.

        Args:
            team_id: Team ID

        Returns:
            List of users
        """
        return self._make_request("GET", f"/api/v2/team/{team_id}/user")

    # ========================================
    # Spaces
    # ========================================

    def get_spaces(self, team_id: str) -> Dict[str, Any]:
        """
        Get all spaces in a team.

        Args:
            team_id: Team ID

        Returns:
            Dictionary with spaces list
        """
        return self._make_request("GET", f"/api/v2/team/{team_id}/space")

    def get_space(self, space_id: str) -> Dict[str, Any]:
        """
        Get a specific space.

        Args:
            space_id: Space ID

        Returns:
            Space data
        """
        return self._make_request("GET", f"/api/v2/space/{space_id}")

    def create_space(
        self,
        team_id: str,
        name: str,
        features: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create a new space.

        Args:
            team_id: Team ID
            name: Space name
            features: Space features configuration

        Returns:
            Created space data
        """
        data = {
            "name": name,
            "features": features or {}
        }
        return self._make_request("POST", f"/api/v2/team/{team_id}/space", data=data)

    def update_space(self, space_id: str, name: str) -> Dict[str, Any]:
        """
        Update a space.

        Args:
            space_id: Space ID
            name: New space name

        Returns:
            Updated space data
        """
        data = {"name": name}
        return self._make_request("PUT", f"/api/v2/space/{space_id}", data=data)

    def delete_space(self, space_id: str) -> Dict[str, Any]:
        """
        Delete a space.

        Args:
            space_id: Space ID

        Returns:
            Deletion confirmation
        """
        return self._make_request("DELETE", f"/api/v2/space/{space_id}")

    # ========================================
    # Folders
    # ========================================

    def get_folders(self, space_id: str) -> Dict[str, Any]:
        """
        Get all folders in a space.

        Args:
            space_id: Space ID

        Returns:
            Dictionary with folders list
        """
        return self._make_request("GET", f"/api/v2/space/{space_id}/folder")

    def get_folder(self, folder_id: str) -> Dict[str, Any]:
        """
        Get a specific folder.

        Args:
            folder_id: Folder ID

        Returns:
            Folder data
        """
        return self._make_request("GET", f"/api/v2/folder/{folder_id}")

    def create_folder(self, space_id: str, name: str) -> Dict[str, Any]:
        """
        Create a new folder.

        Args:
            space_id: Space ID
            name: Folder name

        Returns:
            Created folder data
        """
        data = {"name": name}
        return self._make_request("POST", f"/api/v2/space/{space_id}/folder", data=data)

    def update_folder(self, folder_id: str, name: str) -> Dict[str, Any]:
        """
        Update a folder.

        Args:
            folder_id: Folder ID
            name: New folder name

        Returns:
            Updated folder data
        """
        data = {"name": name}
        return self._make_request("PUT", f"/api/v2/folder/{folder_id}", data=data)

    def delete_folder(self, folder_id: str) -> Dict[str, Any]:
        """
        Delete a folder.

        Args:
            folder_id: Folder ID

        Returns:
            Deletion confirmation
        """
        return self._make_request("DELETE", f"/api/v2/folder/{folder_id}")

    # ========================================
    # Lists
    # ========================================

    def get_lists(self, folder_id: str) -> Dict[str, Any]:
        """
        Get all lists in a folder.

        Args:
            folder_id: Folder ID

        Returns:
            Dictionary with lists
        """
        return self._make_request("GET", f"/api/v2/folder/{folder_id}/list")

    def get_list(self, list_id: str) -> Dict[str, Any]:
        """
        Get a specific list.

        Args:
            list_id: List ID

        Returns:
            List data
        """
        return self._make_request("GET", f"/api/v2/list/{list_id}")

    def create_list(
        self,
        folder_id: str,
        name: str,
        content: str = "",
        due_date: Optional[int] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new list.

        Args:
            folder_id: Folder ID
            name: List name
            content: List description
            due_date: Unix timestamp
            assignees: List of user IDs

        Returns:
            Created list data
        """
        data = {
            "name": name,
            "content": content
        }
        if due_date:
            data["due_date"] = due_date
        if assignees:
            data["assignees"] = assignees

        return self._make_request("POST", f"/api/v2/folder/{folder_id}/list", data=data)

    def update_list(
        self,
        list_id: str,
        name: Optional[str] = None,
        content: Optional[str] = None,
        due_date: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Update a list.

        Args:
            list_id: List ID
            name: New list name
            content: New description
            due_date: New due date (Unix timestamp)

        Returns:
            Updated list data
        """
        data = {}
        if name is not None:
            data["name"] = name
        if content is not None:
            data["content"] = content
        if due_date is not None:
            data["due_date"] = due_date

        return self._make_request("PUT", f"/api/v2/list/{list_id}", data=data)

    def delete_list(self, list_id: str) -> Dict[str, Any]:
        """
        Delete a list.

        Args:
            list_id: List ID

        Returns:
            Deletion confirmation
        """
        return self._make_request("DELETE", f"/api/v2/list/{list_id}")

    # ========================================
    # Tasks
    # ========================================

    def get_tasks(
        self,
        list_id: str,
        page: int = 0,
        order_by: str = "created",
        reverse: bool = False,
        subtasks: bool = False,
        statuses: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        due_date_gt: Optional[int] = None,
        due_date_lt: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get tasks from a list with filtering options.

        Args:
            list_id: List ID
            page: Page number
            order_by: Field to order by
            reverse: Reverse order
            subtasks: Include subtasks
            statuses: Filter by status
            assignees: Filter by assignees
            tags: Filter by tags
            due_date_gt: Due date greater than (Unix timestamp)
            due_date_lt: Due date less than (Unix timestamp)

        Returns:
            Dictionary with tasks
        """
        params = {
            "page": page,
            "order_by": order_by,
            "reverse": "true" if reverse else "false",
            "subtasks": "true" if subtasks else "false"
        }

        if statuses:
            params["statuses"] = ",".join(statuses)
        if assignees:
            params["assignees"] = ",".join(assignees)
        if tags:
            params["tags"] = ",".join(tags)
        if due_date_gt:
            params["due_date_gt"] = due_date_gt
        if due_date_lt:
            params["due_date_lt"] = due_date_lt

        return self._make_request("GET", f"/api/v2/list/{list_id}/task", params=params)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """
        Get a specific task.

        Args:
            task_id: Task ID

        Returns:
            Task data
        """
        return self._make_request("GET", f"/api/v2/task/{task_id}")

    def create_task(
        self,
        list_id: str,
        name: str,
        description: str = "",
        assignees: Optional[List[str]] = None,
        tags: Optional[List[str]] = status,
        priority: Optional[int] = None,
        due_date: Optional[int] = None,
        due_date_time: bool = False,
        parent: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new task.

        Args:
            list_id: List ID
            name: Task name
            description: Task description
            assignees: List of assignee user IDs
            tags: List of tags
            priority: Priority (1-4, where 1 is Urgent)
            due_date: Due date (Unix timestamp)
            due_date_time: Whether due date includes time
            parent: Parent task ID (for subtasks)
            custom_fields: Custom field values

        Returns:
            Created task data
        """
        data = {
            "name": name,
            "description": description,
            "due_date_time": due_date_time
        }

        if assignees:
            data["assignees"] = assignees
        if tags:
            data["tags"] = tags
        if priority is not None:
            data["priority"] = priority
        if due_date:
            data["due_date"] = due_date
        if parent:
            data["parent"] = parent
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("POST", f"/api/v2/list/{list_id}/task", data=data)

    def update_task(
        self,
        task_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        due_date: Optional[int] = None,
        assignees: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update a task.

        Args:
            task_id: Task ID
            name: New task name
            description: New description
            status: New status
            priority: New priority
            due_date: New due date
            assignees: New assignees
            tags: New tags

        Returns:
            Updated task data
        """
        data = {}

        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if status is not None:
            data["status"] = status
        if priority is not None:
            data["priority"] = priority
        if due_date is not None:
            data["due_date"] = due_date
        if assignees is not None:
            data["assignees"] = assignees
        if tags is not None:
            data["tags"] = tags

        return self._make_request("PUT", f"/api/v2/task/{task_id}", data=data)

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            task_id: Task ID

        Returns:
            Deletion confirmation
        """
        return self._make_request("DELETE", f"/api/v2/task/{task_id}")

    def get_task_comments(self, task_id: str) -> Dict[str, Any]:
        """
        Get comments on a task.

        Args:
            task_id: Task ID

        Returns:
            List of comments
        """
        return self._make_request("GET", f"/api/v2/task/{task_id}/comment")

    def create_task_comment(
        self,
        task_id: str,
        comment_text: str,
        assignee: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a comment on a task.

        Args:
            task_id: Task ID
            comment_text: Comment text
            assignee: Assignee user ID

        Returns:
            Created comment data
        """
        data = {
            "comment_text": comment_text
        }
        if assignee:
            data["assignee"] = assignee

        return self._make_request("POST", f"/api/v2/task/{task_id}/comment", data=data)

    # ========================================
    # Time Tracking
    # ========================================

    def get_time_tracking_entries(
        self,
        task_id: str,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get time tracking entries for a task.

        Args:
            task_id: Task ID
            start_date: Start date (Unix timestamp)
            end_date: End date (Unix timestamp)

        Returns:
            List of time entries
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return self._make_request("GET", f"/api/v2/task/{task_id}/time", params=params)

    def create_time_entry(
        self,
        task_id: str,
        duration: int,
        start: int,
        billable: bool = False
    ) -> Dict[str, Any]:
        """
        Create a time tracking entry.

        Args:
            task_id: Task ID
            duration: Duration in milliseconds
            start: Start time (Unix timestamp)
            billable: Whether entry is billable

        Returns:
            Created time entry data
        """
        data = {
            "duration": duration,
            "start": start,
            "billable": billable
        }
        return self._make_request("POST", f"/api/v2/task/{task_id}/time", data=data)

    # ========================================
    # Batch Operations
    # ========================================

    def create_tasks_batch(
        self,
        list_id: str,
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create multiple tasks in batch.

        Args:
            list_id: List ID
            tasks: List of task data dictionaries

        Returns:
            Created tasks data
        """
        data = {"tasks": tasks}
        return self._make_request("POST", f"/api/v2/list/{list_id}/task/batch", data=data)

    def update_tasks_batch(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update multiple tasks in batch.

        Args:
            tasks: List of task update dictionaries with 'id' field

        Returns:
            Updated tasks data
        """
        data = {"tasks": tasks}
        return self._make_request("PUT", "/api/v2/task/batch", data=data)

    # ========================================
    # Webhooks
    # ========================================

    def get_webhooks(self, team_id: str) -> Dict[str, Any]:
        """
        Get all webhooks for a team.

        Args:
            team_id: Team ID

        Returns:
            List of webhooks
        """
        return self._make_request("GET", f"/api/v2/team/{team_id}/webhook")

    def create_webhook(
        self,
        team_id: str,
        endpoint: str,
        events: List[str],
        task_id: Optional[str] = None,
        list_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new webhook.

        Args:
            team_id: Team ID
            endpoint: Webhook endpoint URL
            events: List of events to subscribe to
            task_id: Task ID (optional)
            list_id: List ID (optional)

        Returns:
            Created webhook data
        """
        data = {
            "endpoint": endpoint,
            "events": events
        }
        if task_id:
            data["task_id"] = task_id
        if list_id:
            data["list_id"] = list_id

        return self._make_request("POST", f"/api/v2/team/{team_id}/webhook", data=data)

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Delete a webhook.

        Args:
            webhook_id: Webhook ID

        Returns:
            Deletion confirmation
        """
        return self._make_request("DELETE", f"/api/v2/webhook/{webhook_id}")

    # ========================================
    # Utility Methods
    # ========================================

    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Get current rate limit status.

        Returns:
            Rate limit information
        """
        return {
            "remaining": self.rate_limit_remaining,
            "reset": self.rate_limit_reset,
            "current_time": int(time.time())
        }

    def test_connection(self) -> bool:
        """
        Test API connection by fetching teams.

        Returns:
            True if connection successful
        """
        try:
            response = self.get_teams()
            return "teams" in response
        except ClickUpAPIError:
            return False


def load_clickup_config(config_path: str = "config/clickup-config.json") -> Dict[str, str]:
    """
    Load ClickUp configuration from file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            # Support both direct token and nested structure
            if "api_token" in config:
                return config
            elif "auth" in config and "token" in config["auth"]:
                return {"api_token": config["auth"]["token"]}
    return {"api_token": os.getenv("CLICKUP_API_TOKEN", "")}


def create_clickup_client(config_path: str = "config/clickup-config.json") -> ClickUpAPIClient:
    """
    Create ClickUp API client from configuration.

    Args:
        config_path: Path to configuration file

    Returns:
        Configured ClickUpAPIClient instance

    Raises:
        ValueError: If no API token found
    """
    config = load_clickup_config(config_path)
    api_token = config.get("api_token", "")

    if not api_token:
        raise ValueError(
            "ClickUp API token not found. "
            "Set CLICKUP_API_TOKEN environment variable or create config/clickup-config.json"
        )

    return ClickUpAPIClient(api_token)
