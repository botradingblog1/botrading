import random
import uuid
from ..enums import RiskManagementType


class RiskManagementMethod:
    def __init__(self, id=None, name=None, item_type: RiskManagementType = None, rm_threshold=None, rm_threshold_min=None, rm_threshold_max=None):
        """
        Initializes a new RiskManagementMethod with optional parameters.

        Parameters:
            id (str, optional): The unique identifier of the method. Defaults to a UUID.
            name (str, optional): The name of the method. Defaults to "Default Name".
            item_type (RiskManagementType, optional): The type of risk management. Defaults to RiskManagementType.DEFAULT.
            rm_threshold (int, optional): The risk management threshold. Defaults to 0.
            rm_threshold_min (int, optional): The minimum risk management threshold. Defaults to 0.
            rm_threshold_max (int, optional): The maximum risk management threshold. Defaults to 100.
        """
        self.id = id if id is not None else str(uuid.uuid4())
        self.name = name if name is not None else "Default Name"
        self.item_type = item_type if item_type is not None else RiskManagementType.DEFAULT
        self.rm_threshold = rm_threshold if rm_threshold is not None else 0
        self.rm_threshold_min = rm_threshold_min if rm_threshold_min is not None else 0
        self.rm_threshold_max = rm_threshold_max if rm_threshold_max is not None else 100

    def randomize(self):
        """
        Randomizes the risk management parameters within the specified min and max thresholds.
        """
        self.rm_threshold = random.randint(self.rm_threshold_min, self.rm_threshold_max)

