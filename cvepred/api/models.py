from pydantic import BaseModel
import typing as ty


class CveModel(BaseModel):
    attackVector: ty.Literal["NETWORK", "ADJACENT_NETWORK", "LOCAL", "PHYSICAL"]
    attackComplexity: ty.Literal["LOW", "HIGH"]
    privilegesRequired: ty.Literal["NONE", "LOW", "HIGH"]
    userInteraction: ty.Literal["NONE", "REQUIRED"]
    scope: ty.Literal["UNCHANGED", "CHANGED"]
    confidentialityImpact: ty.Literal["NONE", "LOW", "HIGH"]
    integrityImpact: ty.Literal["NONE", "LOW", "HIGH"]
    availabilityImpact: ty.Literal["NONE", "LOW", "HIGH"]
    # hasExploit: bool


class CveModels(BaseModel):
    data: ty.List[CveModel]


class CveNvdIdsModel(BaseModel):
    ids: ty.List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ids": [
                        "CVE-2016-2183",
                        "CVE-2021-3438",
                        # "CVE-2016-2137",
                    ]
                }
            ]
        }
    }
