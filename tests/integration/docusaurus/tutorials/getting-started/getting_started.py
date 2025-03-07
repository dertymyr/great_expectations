import great_expectations as gx
from great_expectations.core.batch import BatchRequest
from great_expectations.core.yaml_handler import YAMLHandler
from great_expectations.profile.user_configurable_profiler import (
    UserConfigurableProfiler,
)
from great_expectations.validator.validator import Validator

yaml = YAMLHandler()
context = gx.get_context()
# NOTE: The following assertion is only for testing and can be ignored by users.
assert context

# First configure a new Datasource and add to DataContext

# <snippet name="tests/integration/docusaurus/tutorials/getting-started/getting_started.py datasource_yaml">
datasource_yaml = """
name: getting_started_datasource
class_name: Datasource
execution_engine:
  class_name: PandasExecutionEngine
data_connectors:
    default_inferred_data_connector_name:
        class_name: InferredAssetFilesystemDataConnector
        base_directory: ../data/
        default_regex:
          group_names:
            - data_asset_name
          pattern: (.*)
    default_runtime_data_connector_name:
        class_name: RuntimeDataConnector
        assets:
            my_runtime_asset_name:
              batch_identifiers:
                - runtime_batch_identifier_name
"""
# </snippet>

context.test_yaml_config(datasource_yaml)
context.add_datasource(**yaml.load(datasource_yaml))

# Get Validator by creating ExpectationSuite and passing in BatchRequest
batch_request = BatchRequest(
    datasource_name="getting_started_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="yellow_tripdata_sample_2019-01.csv",
    limit=1000,
)

expectation_suite_name = "getting_started_expectation_suite_taxi.demo"

context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)

validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name=expectation_suite_name
)

# NOTE: The following assertion is only for testing and can be ignored by users.
assert isinstance(validator, Validator)

# Profile the data with the UserConfigurableProfiler and save resulting ExpectationSuite
exclude_column_names = [
    "vendor_id",
    "pickup_datetime",
    "dropoff_datetime",
    # "passenger_count",
    "trip_distance",
    "rate_code_id",
    "store_and_fwd_flag",
    "pickup_location_id",
    "dropoff_location_id",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
]

profiler = UserConfigurableProfiler(
    profile_dataset=validator,
    excluded_expectations=None,
    ignored_columns=exclude_column_names,
    not_null_only=False,
    primary_or_compound_key=None,
    semantic_types_dict=None,
    table_expectations_only=False,
    value_set_threshold="MANY",
)
suite = profiler.build_suite()
validator.expectation_suite = suite
validator.save_expectation_suite(discard_failed_expectations=False)

# Create first checkpoint on yellow_tripdata_sample_2019-01.csv
my_checkpoint_config = """
name: getting_started_checkpoint
validations:
  - batch_request:
      datasource_name: getting_started_datasource
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: yellow_tripdata_sample_2019-01.csv
      data_connector_query:
        index: -1
    expectation_suite_name: getting_started_expectation_suite_taxi.demo
"""
my_checkpoint_config = yaml.load(my_checkpoint_config)

# NOTE: The following code (up to and including the assert) is only for testing and can be ignored by users.
# In the current test, an action_list without a build data docs is passed to .run because we do not want to update
# and build data_docs
checkpoint = context.add_or_update_checkpoint(
    **my_checkpoint_config,
    action_list=[
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {
            "name": "store_evaluation_params",
            "action": {"class_name": "StoreEvaluationParametersAction"},
        },
    ],
)
checkpoint_result = checkpoint.run()
assert checkpoint_result.run_results


# Create second checkpoint on yellow_tripdata_sample_2019-02.csv
# <snippet name="tests/integration/docusaurus/tutorials/getting-started/getting_started.py checkpoint_yaml_config">
yaml_config = """
name: getting_started_checkpoint
validations:
  - batch_request:
      datasource_name: getting_started_datasource
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: yellow_tripdata_sample_2019-02.csv
      data_connector_query:
        index: -1
    expectation_suite_name: getting_started_expectation_suite_taxi.demo
"""
# </snippet>

my_new_checkpoint_config = yaml.load(yaml_config)

# NOTE: The following code (up to and including the assert) is only for testing and can be ignored by users.
# In the current test, an action_list without a build data docs is passed to .run because we do not want to update
# and build data_docs
new_checkpoint = context.add_or_update_checkpoint(
    **my_new_checkpoint_config,
    action_list=[
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {
            "name": "store_evaluation_params",
            "action": {"class_name": "StoreEvaluationParametersAction"},
        },
    ],
)
new_checkpoint_result = new_checkpoint.run()
assert new_checkpoint_result.run_results
