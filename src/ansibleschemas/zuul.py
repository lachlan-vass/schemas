# Used to generate JSON Validations schema for Zuul config files.
import sys
from typing import Any, List, Mapping, Optional, Union

from pydantic import BaseModel, Extra, Field

from . import consts

if sys.version_info >= (3, 8):
    from typing import Literal  # pylint: disable=no-name-in-module
else:
    from typing_extensions import Literal


class PipelineModel(BaseModel):
    jobs: Optional[List[Any]]
    queue: Optional[str]

    class Config:
        extra = Extra.forbid


class ProjectBaseModel(BaseModel):

    description: Optional[str]
    vars: Optional[Mapping[str, Any]]
    default_branch: Optional[str] = Field(alias="default-branch")
    # For the moment we hardcode common pipeline names, until we figure out
    # a way to distinguish pipelines from other properties.
    post: Optional[PipelineModel]
    release: Optional[PipelineModel]
    check: Optional[PipelineModel]
    gate: Optional[PipelineModel]
    promote: Optional[PipelineModel]
    periodic_weekly: Optional[PipelineModel] = Field(alias="periodic-weekly")
    third_party_check: Optional[PipelineModel] = Field(alias="third-party-check")


class ProjectTemplateModel(ProjectBaseModel):
    name: str

    class Config:
        extra = Extra.forbid


class ProjectModel(ProjectBaseModel):
    name: Optional[str]
    templates: Optional[List[str]]

    class Config:
        extra = Extra.forbid


class SecretModel(BaseModel):
    name: str
    data: Mapping[str, Any]

    class Config:
        extra = Extra.forbid


class JobSecretModel(BaseModel):
    name: str
    secret: str
    pass_to_parent: Optional[bool] = Field(alias="pass-to-parent", default=False)

    class Config:
        extra = Extra.forbid


class JobModel(BaseModel):
    # based on https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html#play
    name: str
    description: Optional[str]
    pre_run: Optional[Union[str, List[str]]] = Field(alias="pre-run")
    post_run: Optional[Union[str, List[str]]] = Field(alias="post-run")
    run: Optional[str]
    nodeset: Optional[Any]
    parent: Optional[str]
    vars: Optional[Mapping[str, Any]]
    files: Optional[Union[str, List[str]]]
    override_checkout: Optional[str] = Field(alias="override-checkout")
    success_url: Optional[str] = Field(alias="success-url")
    abstract: Optional[bool] = False
    voting: Optional[bool] = True
    timeout: Optional[int]
    ansible_version: Optional[
        Union[float, Literal["2.7", "2.8", "2.9", "2.10", "2.11"]]
    ] = Field(alias="ansible-version")
    host_vars: Optional[Mapping[str, Mapping[str, Any]]] = Field(alias="host-vars")
    tags: Optional[Union[str, List[str]]]
    required_projects: Optional[List[str]] = Field(alias="required-projects")
    secrets: Optional[Union[JobSecretModel, List[Union[JobSecretModel, str]]]]

    class Config:
        extra = Extra.forbid


class JobEntry(BaseModel):
    # based on https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html#play
    job: JobModel

    class Config:
        extra = Extra.forbid


class ProjectTemplateEntry(BaseModel):
    # based on https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html#play
    project_template: ProjectTemplateModel = Field(alias="project-template")

    class Config:
        extra = Extra.forbid


class ProjectEntry(BaseModel):
    # based on https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html#play
    project: ProjectModel

    class Config:
        extra = Extra.forbid


class SecretEntry(BaseModel):
    secret: SecretModel

    class Config:
        extra = Extra.forbid


class ZuulConfigModel(BaseModel):
    __root__: List[Union[JobEntry, ProjectEntry, ProjectTemplateEntry, SecretEntry]]

    class Config:
        extra = Extra.forbid
        title = "Zuul Config Schema"
        schema_extra = {
            "$schema": consts.META_SCHEMA_URI,
        }
