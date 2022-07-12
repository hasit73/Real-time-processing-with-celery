import random

from real_time_celery.utils import util


class RandomDataGenerator:
    def __init__(
        self, objects_list_file="real_time_celery/static-data/objects_list.txt"
    ):
        self.__colors = ["Red", "Blue", "Yellow", "Green", "Pink", "Purple"]
        self.__objects = []
        with open(objects_list_file, "r") as objects_file:
            self.__objects = [s.strip() for s in objects_file.readlines() if s.strip()]
        self.__object_size_list = ["0.5X", "1.0X", "1.5X", "2.0X", "3.0X", "5.0X"]
        self.__rigidness = ["Low", "Medium", "High"]

    def get_constants(self):
        """Get class field values of object.

        Returns:
            tuple: Values.
        """
        return (
            self.__colors,
            self.__objects,
            self.__object_size_list,
            self.__rigidness,
        )

    @util.compute_time
    def generate_data(self, samples=1000):
        """Generate random data.

        Args:
            samples (int, optional): number of samples. Defaults to 1000.

        Returns:
            dict: List of generated data.
        """
        response = {}
        data_colors = random.choices(self.__colors, k=samples)
        data_objects = random.choices(self.__objects, k=samples)
        data_objects_size = random.choices(self.__object_size_list, k=samples)
        data_rigidity = random.choices(self.__rigidness, k=samples)
        response["data"] = [
            {"object": object, "color": color, "rigidity": rigidity, "size": size}
            for (object, color, size, rigidity) in zip(
                data_objects, data_colors, data_objects_size, data_rigidity
            )
        ]
        return response
