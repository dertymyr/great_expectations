import os

import great_expectations as gx
from great_expectations.core.expectation_validation_result import (
    ExpectationSuiteValidationResult,
)
from great_expectations.core.run_identifier import RunIdentifier
from great_expectations.core.yaml_handler import YAMLHandler
from great_expectations.data_context.types.base import CheckpointConfig
from great_expectations.data_context.types.resource_identifiers import (
    ValidationResultIdentifier,
)
from great_expectations.datasource.fluent import (
    BatchRequest as FluentBatchRequest,
)

yaml = YAMLHandler()
context = gx.get_context()

# Add datasource for all tests
context.sources.add_pandas_filesystem(
    "taxi_datasource",
    base_directory="./data",
).add_csv_asset(
    "taxi_asset",
    batching_regex=r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2})\.csv",
)

assert [ds["name"] for ds in context.list_datasources()] == ["taxi_datasource"]
context.add_or_update_expectation_suite("my_expectation_suite")
context.add_or_update_expectation_suite("my_other_expectation_suite")

# Add a Checkpoint
context.add_or_update_checkpoint(
    name="test_checkpoint",
    validations=[
        {
            "batch_request": {
                "datasource_name": "taxi_datasource",
                "data_asset_name": "taxi_asset",
                "options": {"year": "2019", "month": "01"},
            },
            "expectation_suite_name": "my_expectation_suite",
            "action_list": [
                {
                    "name": "<ACTION NAME FOR STORING VALIDATION RESULTS>",
                    "action": {"class_name": "StoreValidationResultAction"},
                },
                {
                    "name": "<ACTION NAME FOR STORING EVALUATION PARAMETERS>",
                    "action": {"class_name": "StoreEvaluationParametersAction"},
                },
                {
                    "name": "<ACTION NAME FOR UPDATING DATA DOCS>",
                    "action": {"class_name": "UpdateDataDocsAction"},
                },
            ],
        }
    ],
)
assert context.list_checkpoints() == ["test_checkpoint"]

checkpoint = context.get_checkpoint("test_checkpoint")
results = checkpoint.run()
assert results.success is True
run_id_type = type(results.run_id)
assert run_id_type == RunIdentifier
validation_result_id_type_set = {type(k) for k in results.run_results.keys()}
assert len(validation_result_id_type_set) == 1
validation_result_id_type = next(iter(validation_result_id_type_set))
assert validation_result_id_type == ValidationResultIdentifier
validation_result_id = results.run_results[[k for k in results.run_results.keys()][0]]
assert (
    type(validation_result_id["validation_result"]) is ExpectationSuiteValidationResult
)
assert isinstance(results.checkpoint_config, CheckpointConfig)

typed_results = {
    "run_id": run_id_type,
    "run_results": {
        validation_result_id_type: {
            "validation_result": type(validation_result_id["validation_result"]),
            "actions_results": {
                "<ACTION NAME FOR STORING VALIDATION RESULTS>": {
                    "class": "StoreValidationResultAction"
                }
            },
        }
    },
    "checkpoint_config": CheckpointConfig,
    "success": True,
}

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py results">
results = {
    "run_id": RunIdentifier,
    "run_results": {
        ValidationResultIdentifier: {
            "validation_result": ExpectationSuiteValidationResult,
            "actions_results": {
                "<ACTION NAME FOR STORING VALIDATION RESULTS>": {
                    "class": "StoreValidationResultAction"
                }
            },
        }
    },
    "checkpoint_config": CheckpointConfig,
    "success": True,
}
# </snippet>

assert typed_results == results

# A few different Checkpoint examples
os.environ["VAR"] = "ge"

batch_request = FluentBatchRequest(
    datasource_name="taxi_datasource",
    data_asset_name="taxi_asset",
    options={"year": "2019", "month": "01"},
)
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name="my_expectation_suite"
)
validator.expect_table_row_count_to_be_between(
    min_value={"$PARAMETER": "GT_PARAM", "$PARAMETER.GT_PARAM": 0},
    max_value={"$PARAMETER": "LT_PARAM", "$PARAMETER.LT_PARAM": 1000000},
)
validator.save_expectation_suite(discard_failed_expectations=False)
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name="my_other_expectation_suite"
)
validator.expect_table_row_count_to_be_between(
    min_value={"$PARAMETER": "GT_PARAM", "$PARAMETER.GT_PARAM": 0},
    max_value={"$PARAMETER": "LT_PARAM", "$PARAMETER.LT_PARAM": 1000000},
)
validator.save_expectation_suite(discard_failed_expectations=False)

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py no_nesting">
# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py no_nesting just the yaml">
context.add_or_update_checkpoint(
    name="my_checkpoint",
    validations=[
        {
            "batch_request": {
                "datasource_name": "taxi_datasource",
                "data_asset_name": "taxi_asset",
                "options": {"year": "2019", "month": "01"},
            },
            "expectation_suite_name": "my_expectation_suite",
            "action_list": [
                {
                    "name": "<ACTION NAME FOR STORING VALIDATION RESULTS>",
                    "action": {"class_name": "StoreValidationResultAction"},
                },
                {
                    "name": "<ACTION NAME FOR STORING EVALUATION PARAMETERS>",
                    "action": {"class_name": "StoreEvaluationParametersAction"},
                },
                {
                    "name": "<ACTION NAME FOR UPDATING DATA DOCS>",
                    "action": {"class_name": "UpdateDataDocsAction"},
                },
            ],
        }
    ],
    evaluation_parameters={"GT_PARAM": 1000, "LT_PARAM": 50000},
    runtime_configuration={
        "result_format": {"result_format": "BASIC", "partial_unexpected_count": 20}
    },
)
# </snippet>
# </snippet>

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py run_checkpoint">
checkpoint = context.get_checkpoint("my_checkpoint")
results = checkpoint.run()
# </snippet>
assert results.success is True
assert (
    list(results.run_results.items())[0][1]["validation_result"]["results"][0][
        "expectation_config"
    ]["kwargs"]["max_value"]
    == 50000
)
assert (
    list(results.run_results.items())[0][1]["validation_result"]["results"][0][
        "expectation_config"
    ]["kwargs"]["min_value"]
    == 1000
)

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py nesting_with_defaults">
# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py nesting_with_defaults just the yaml">
context.add_or_update_checkpoint(
    name="my_checkpoint",
    validations=[
        {
            "batch_request": {
                "datasource_name": "taxi_datasource",
                "data_asset_name": "taxi_asset",
                "options": {"year": "2019", "month": "01"},
            },
        },
        {
            "batch_request": {
                "datasource_name": "taxi_datasource",
                "data_asset_name": "taxi_asset",
                "options": {"year": "2019", "month": "02"},
            },
        },
    ],
    expectation_suite_name="my_expectation_suite",
    action_list=[
        {
            "name": "<ACTION NAME FOR STORING VALIDATION RESULTS>",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {
            "name": "<ACTION NAME FOR STORING EVALUATION PARAMETERS>",
            "action": {"class_name": "StoreEvaluationParametersAction"},
        },
        {
            "name": "<ACTION NAME FOR UPDATING DATA DOCS>",
            "action": {"class_name": "UpdateDataDocsAction"},
        },
    ],
    evaluation_parameters={"GT_PARAM": 1000, "LT_PARAM": 50000},
    runtime_configuration={
        "result_format": {"result_format": "BASIC", "partial_unexpected_count": 20}
    },
)
# </snippet>
# </snippet>

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py run_checkpoint_2">
checkpoint = context.get_checkpoint("my_checkpoint")
results = checkpoint.run()
# </snippet>
assert results.success is True

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py validation_results_suites_data_assets">
first_validation_result = list(results.run_results.items())[0][1]["validation_result"]
second_validation_result = list(results.run_results.items())[1][1]["validation_result"]

first_expectation_suite = first_validation_result["meta"]["expectation_suite_name"]
first_data_asset = first_validation_result["meta"]["active_batch_definition"][
    "data_asset_name"
]
second_expectation_suite = second_validation_result["meta"]["expectation_suite_name"]
second_data_asset = second_validation_result["meta"]["active_batch_definition"][
    "data_asset_name"
]
first_batch_identifiers = first_validation_result["meta"]["active_batch_definition"][
    "batch_identifiers"
]
second_batch_identifiers = second_validation_result["meta"]["active_batch_definition"][
    "batch_identifiers"
]

assert first_expectation_suite == "my_expectation_suite"
assert first_data_asset == "taxi_asset"
assert first_batch_identifiers == {
    "path": "yellow_tripdata_sample_2019-01.csv",
    "year": "2019",
    "month": "01",
}

assert second_expectation_suite == "my_expectation_suite"
assert second_data_asset == "taxi_asset"
assert second_batch_identifiers == {
    "path": "yellow_tripdata_sample_2019-02.csv",
    "year": "2019",
    "month": "02",
}
# </snippet>

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py keys_passed_at_runtime">
# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py keys_passed_at_runtime just the yaml">
context.add_or_update_checkpoint(
    name="my_base_checkpoint",
    action_list=[
        {
            "name": "<ACTION NAME FOR STORING VALIDATION RESULTS>",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {
            "name": "<ACTION NAME FOR STORING EVALUATION PARAMETERS>",
            "action": {"class_name": "StoreEvaluationParametersAction"},
        },
        {
            "name": "<ACTION NAME FOR UPDATING DATA DOCS>",
            "action": {"class_name": "UpdateDataDocsAction"},
        },
    ],
    evaluation_parameters={"GT_PARAM": 1000, "LT_PARAM": 50000},
    runtime_configuration={
        "result_format": {"result_format": "BASIC", "partial_unexpected_count": 20}
    },
)
# </snippet>
# </snippet>

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py run_checkpoint_3">
checkpoint = context.get_checkpoint("my_base_checkpoint")
results = checkpoint.run(
    validations=[
        {
            "batch_request": {
                "datasource_name": "taxi_datasource",
                "data_asset_name": "taxi_asset",
                "options": {"year": "2019", "month": "01"},
            },
            "expectation_suite_name": "my_expectation_suite",
        },
        {
            "batch_request": {
                "datasource_name": "taxi_datasource",
                "data_asset_name": "taxi_asset",
                "options": {"year": "2019", "month": "02"},
            },
            "expectation_suite_name": "my_other_expectation_suite",
        },
    ],
)
# </snippet>
assert results.success is True
# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py validation_results_suites_data_assets_2">
first_validation_result = list(results.run_results.items())[0][1]["validation_result"]
second_validation_result = list(results.run_results.items())[1][1]["validation_result"]

first_expectation_suite = first_validation_result["meta"]["expectation_suite_name"]
first_data_asset = first_validation_result["meta"]["active_batch_definition"][
    "data_asset_name"
]
first_batch_identifiers = first_validation_result["meta"]["active_batch_definition"][
    "batch_identifiers"
]
second_expectation_suite = second_validation_result["meta"]["expectation_suite_name"]
second_data_asset = second_validation_result["meta"]["active_batch_definition"][
    "data_asset_name"
]
second_batch_identifiers = second_validation_result["meta"]["active_batch_definition"][
    "batch_identifiers"
]

assert first_expectation_suite == "my_expectation_suite"
assert first_data_asset == "taxi_asset"
assert first_batch_identifiers == {
    "path": "yellow_tripdata_sample_2019-01.csv",
    "year": "2019",
    "month": "01",
}

assert second_expectation_suite == "my_other_expectation_suite"
assert second_data_asset == "taxi_asset"
assert second_batch_identifiers == {
    "path": "yellow_tripdata_sample_2019-02.csv",
    "year": "2019",
    "month": "02",
}
# </snippet>

context.add_or_update_expectation_suite("my_expectation_suite")
context.add_or_update_expectation_suite("my_other_expectation_suite")

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py using_template">
# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py using_template just the yaml">
context.add_or_update_checkpoint(
    name="my_checkpoint",
    validations=[
        {
            "batch_request": {
                "datasource_name": "taxi_datasource",
                "data_asset_name": "taxi_asset",
                "options": {"year": "2019", "month": "01"},
            },
            "expectation_suite_name": "my_expectation_suite",
        },
        {
            "batch_request": {
                "datasource_name": "taxi_datasource",
                "data_asset_name": "taxi_asset",
                "options": {"year": "2019", "month": "02"},
            },
            "expectation_suite_name": "my_other_expectation_suite",
        },
    ],
)
# </snippet>
# </snippet>

# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py run_checkpoint_4">
checkpoint = context.get_checkpoint("my_checkpoint")
results = checkpoint.run()
# </snippet>
assert results.success is True
# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py validation_results_suites_data_assets_3">
first_validation_result = list(results.run_results.items())[0][1]["validation_result"]
second_validation_result = list(results.run_results.items())[1][1]["validation_result"]

first_expectation_suite = first_validation_result["meta"]["expectation_suite_name"]
first_data_asset = first_validation_result["meta"]["active_batch_definition"][
    "data_asset_name"
]
first_batch_identifiers = first_validation_result["meta"]["active_batch_definition"][
    "batch_identifiers"
]
second_expectation_suite = second_validation_result["meta"]["expectation_suite_name"]
second_data_asset = second_validation_result["meta"]["active_batch_definition"][
    "data_asset_name"
]
second_batch_identifiers = second_validation_result["meta"]["active_batch_definition"][
    "batch_identifiers"
]

assert first_expectation_suite == "my_expectation_suite"
assert first_data_asset == "taxi_asset"
assert first_batch_identifiers == {
    "path": "yellow_tripdata_sample_2019-01.csv",
    "year": "2019",
    "month": "01",
}

assert second_expectation_suite == "my_other_expectation_suite"
assert second_data_asset == "taxi_asset"
assert second_batch_identifiers == {
    "path": "yellow_tripdata_sample_2019-02.csv",
    "year": "2019",
    "month": "02",
}
# </snippet>

equivalent_using_checkpoint = """
# <snippet name="docs/docusaurus/docs/snippets/checkpoints_and_actions.py checkpoint_example">
name: my_checkpoint
validations:
  - batch_request:
      datasource_name: taxi_datasource
      data_asset_name: taxi_asset
      options:
        year: "2019"
        month: "01"
    expectation_suite_name: my_expectation_suite
action_list:
  - name: store_validation_result
    action:
      class_name: StoreValidationResultAction
  - name: store_evaluation_params
    action:
      class_name: StoreEvaluationParametersAction
  - name: update_data_docs
    action:
      class_name: UpdateDataDocsAction
  - name: send_slack_notification
    action:
      class_name: SlackNotificationAction
      slack_webhook: <YOUR SLACK WEBHOOK URL>
      notify_on: failure
      notify_with: all
      renderer:
        module_name: great_expectations.render.renderer.slack_renderer
        class_name: SlackRenderer
"""
checkpoint_example = equivalent_using_checkpoint.replace(
    "<YOUR SLACK WEBHOOK URL>", "https://hooks.slack.com/foo/bar"
)
context.add_or_update_checkpoint(**yaml.load(equivalent_using_checkpoint))
context.add_or_update_checkpoint(**yaml.load(checkpoint_example))

checkpoint = context.get_checkpoint("my_checkpoint")
results = checkpoint.run()

assert results.success is True
validation_result = list(results.run_results.items())[0][1]["validation_result"]

expectation_suite = validation_result["meta"]["expectation_suite_name"]
data_asset = validation_result["meta"]["active_batch_definition"]["data_asset_name"]
batch_identifiers = validation_result["meta"]["active_batch_definition"][
    "batch_identifiers"
]

assert expectation_suite == "my_expectation_suite"
assert data_asset == "taxi_asset"
assert batch_identifiers == {
    "path": "yellow_tripdata_sample_2019-01.csv",
    "year": "2019",
    "month": "01",
}
