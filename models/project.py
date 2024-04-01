import json
from typing import Dict, Any, Optional
import os
from settings import PROJECT_DIR


class Project:
    """
    Class representing the project, in other words, canvas in dictionary
    """

    def __init__(self, project_name: str):
        """
        Initializes the project
        :param project_name: name of the project
        """
        self.__project_name = project_name

    def open(self) -> Optional[Dict[str, Any]]:
        """
        Opens the last project from json file
        :return: saved canvas as a dictionary
        """
        try:
            path = os.path.join(PROJECT_DIR, self.__project_name)
            f = open(path, 'r')
            data = json.load(f)
            f.close()
            print('Project opened. Loading to canvas...')
            return data
        except FileNotFoundError:
            print('Project not found. Creating new one...')
            return None

    def save(self, saved_canvas: Dict[Any, Any]) -> None:
        """
        Saves the current project to json file
        :param saved_canvas: saved canvas as a dictionary
        :return: None
        """
        path = os.path.join(PROJECT_DIR, self.__project_name)
        f = open(path, 'w')
        json.dump(saved_canvas, f)
        f.close()
