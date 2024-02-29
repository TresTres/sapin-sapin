from backend.models.base import *
from backend.models.data import *


class Tag(BaseModel):
    """
    Represents a tag that can be associated with an entity.
    TODO: Expand this if necessary and hook up to data models
    """
    name = CharField(null=False, unique=True, constraints=[Check("length(name) > 0"), Check("length(name) < 50")])

    def save(self, *args, **kwargs) -> int:
        """
        Override the save method to conduct validations.
        Name must be non-empty and will be converted to lowercase.
        """
        if not self.name:
            raise ValidationError("Name must be non-empty")
        self.name = self.name.strip().lower()
        return super().save(*args, **kwargs)