from real_time_celery.utils import util
from real_time_celery.utils.data_generator import RandomDataGenerator


class DataProcessor:
    def __init__(self):
        self.generator = RandomDataGenerator()
        (
            self.colors,
            self.objects,
            self.object_size_list,
            self.rigidness,
        ) = self.generator.get_constants()
        self.colors_mapping = dict(zip(self.colors, range(len(self.colors))))
        self.objects_mapping = dict(zip(self.objects, range(len(self.objects))))
        self.object_size_mapping = dict(
            zip(self.object_size_list, range(len(self.object_size_list)))
        )
        self.rigidness_mapping = dict(zip(self.rigidness, range(len(self.rigidness))))

    @util.compute_time
    def process_data(self, data):
        """Encodes input data by fixed numbers.

        Args:
            data (dict): Input data.

        Returns:
            dict: Encoded data.
        """
        processed_data = []
        for record in data.get("data", []):
            processed_data.append(
                {
                    "object_label": record.get("object", -1),
                    "color_label": record.get("color", -1),
                    "size_label": record.get("size", -1),
                    "rigidity_label": record.get("rigidity", -1),
                }
            )
        response = {"data": processed_data}
        return response
