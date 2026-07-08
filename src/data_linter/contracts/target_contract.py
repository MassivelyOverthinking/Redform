#########################################################################################################
# IMPORTS
#########################################################################################################

from .basemodel import RedformBaseModel
from ..aliases import TargetType, ScalarValue
from pydantic import Field, model_validator

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> TARGET (ML/AI)
#########################################################################################################

class TargetContract(RedformBaseModel):
    column: str
    type: TargetType

    required_classes: list[ScalarValue] | None = None
    min_class_ratio: float | None = Field(default=None, ge=0, le=1) 
    max_class_ratio: float | None = Field(default=None, ge=0, le=1) 
    
    min: int | float | None = None
    max: int | float | None = None
    max_null_ratio: float | None = Field(default=None, ge=0, le=1)

    @model_validator(mode="after")
    def validate_target_bounds(self) -> "TargetContract":
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("Target min cannot be greater than Target max")
        
        if (
            self.min_class_ratio is not None
            and self.max_class_ratio is not None
            and self.min_class_ratio > self.max_class_ratio
        ):
            raise ValueError("Min_class_ratio cannot be greater than max_class_ratio")
        
        if self.type == "classification" and self.required_classes is not None:
            if len(self.required_classes) == 0:
                raise ValueError("Required_classea cannot be an empty list")
            
        if self.type == "regression" and self.required_classes is not None:
            raise ValueError("required_classes can only be used for classification targets")
        
        return self