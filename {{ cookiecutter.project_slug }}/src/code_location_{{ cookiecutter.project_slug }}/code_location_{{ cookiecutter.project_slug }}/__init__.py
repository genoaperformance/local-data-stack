from pathlib import Path

from dagster import (
    AutomationCondition,
    Definitions,
    link_code_references_to_git,
    load_asset_checks_from_package_module,
    load_assets_from_package_module,
    with_source_code_references,
)
from dagster._core.definitions.metadata.source_code import AnchorBasedFilePathMapping

# from dagster_cloud.metadata.source_code import link_code_references_to_git_if_cloud
from {{ cookiecutter.project_slug }} import assets

from .resources import get_resources_for_deployment

resource_defs = get_resources_for_deployment()
all_assets = with_source_code_references(
    [
        *load_assets_from_package_module(
            assets,
            automation_condition=AutomationCondition.eager(),
        ),
    ]
)
all_asset_checks = [*load_asset_checks_from_package_module(assets)]

all_assets = link_code_references_to_git(
    assets_defs=all_assets,
    git_url="https://github.com/{{ cookiecutter.organization }}/{{ cookiecutter.project_slug }}/",
    git_branch="main",
    file_path_mapping=AnchorBasedFilePathMapping(
        local_file_anchor=Path(__file__).parent,
        file_anchor_path_in_repository="src/{{ cookiecutter.project_slug }}",
    ),
)
# requires env vars for git hash to be set - but then it is more flexible see .env example
# all_assets = link_code_references_to_git_if_cloud(
#     assets_defs=with_source_code_references(
#         [
#             *load_assets_from_package_module(assets),
#         ]
#     ),
#     # Inferred from searching for .git directory in parent directories
#     # of the module containing this code - may also be set explicitly
#     file_path_mapping=AnchorBasedFilePathMapping(
#         local_file_anchor=Path(__file__),
#         file_anchor_path_in_repository="prototyping/tech-exploration/dagster/src/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}/__init__.py",
#     ),
# )


defs = Definitions(
    assets=all_assets,
    asset_checks=all_asset_checks,
    schedules=[],
    sensors=[],
    jobs=[],
    resources=resource_defs,
)
