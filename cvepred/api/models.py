from pydantic import BaseModel
import typing as ty

# attackVector             category
# attackComplexity         category
# privilegesRequired       category
# userInteraction          category
# scope                    category
# confidentialityImpact    category
# integrityImpact          category
# availabilityImpact       category
# hasExploit                   bool


class CveModel(BaseModel):
    attackVector: str
    attackComplexity: str
    privilegesRequired: str
    userInteraction: str
    scope: str
    confidentialityImpact: str
    integrityImpact: str
    availabilityImpact: str
    # hasExploit: bool


class CveModels(BaseModel):
    data: ty.List[CveModel]
