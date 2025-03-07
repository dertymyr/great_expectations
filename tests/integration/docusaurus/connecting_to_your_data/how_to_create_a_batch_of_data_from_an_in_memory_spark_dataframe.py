# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py imports">
import great_expectations as gx
from great_expectations.compatibility import pyspark
from great_expectations.core import ExpectationSuite
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.core.yaml_handler import YAMLHandler
from great_expectations.data_context.util import file_relative_path
from great_expectations.execution_engine import SparkDFExecutionEngine
from great_expectations.validator.validator import Validator

yaml = YAMLHandler()
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py get_context">
context = gx.get_context()
# </snippet>

spark_session: pyspark.SparkSession = (
    SparkDFExecutionEngine.get_or_create_spark_session()
)

# create and load Expectation Suite
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py create_expectation_suite">
context.add_expectation_suite(
    expectation_suite_name="insert_your_expectation_suite_name_here"
)
# </snippet>
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py get_expectation_suite">
suite: ExpectationSuite = context.get_expectation_suite(
    expectation_suite_name="insert_your_expectation_suite_name_here"
)
# </snippet>
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py datasource_yaml">
datasource_yaml = """
name: my_spark_datasource
class_name: Datasource
module_name: great_expectations.datasource
execution_engine:
    module_name: great_expectations.execution_engine
    class_name: SparkDFExecutionEngine
data_connectors:
    my_runtime_data_connector:
        class_name: RuntimeDataConnector
        batch_identifiers:
            - some_key_maybe_pipeline_stage
            - some_other_key_maybe_airflow_run_id
"""
# </snippet>
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py add_datasource">
context.add_datasource(**yaml.load(datasource_yaml))
# </snippet>
# RuntimeBatchRequest with batch_data as Spark Dataframe
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py path_to_file">
path_to_file: str = "some_path.csv"
# </snippet>
# Please note this override is only to provide good UX for docs and tests.
path_to_file: str = file_relative_path(
    __file__, "data/yellow_tripdata_sample_2019-01.csv"
)
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py pyspark_df">
df: pyspark.DataFrame = spark_session.read.csv(path_to_file)
# </snippet>
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py runtime_batch_request">
runtime_batch_request = RuntimeBatchRequest(
    datasource_name="my_spark_datasource",
    data_connector_name="my_runtime_data_connector",
    data_asset_name="insert_your_data_asset_name_here",
    runtime_parameters={"batch_data": df},
    batch_identifiers={
        "some_key_maybe_pipeline_stage": "ingestion step 1",
        "some_other_key_maybe_airflow_run_id": "run 18",
    },
)
# </snippet>

# Please note this override is only to provide good UX for docs and tests.
path_to_file: str = file_relative_path(
    __file__, "data/yellow_tripdata_sample_2019-01.csv"
)

# RuntimeBatchRequest with path
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py runtime_batch_request_2">
runtime_batch_request = RuntimeBatchRequest(
    datasource_name="my_spark_datasource",
    data_connector_name="my_runtime_data_connector",
    data_asset_name="insert_your_data_asset_name_here",
    runtime_parameters={"path": path_to_file},
    batch_identifiers={
        "some_key_maybe_pipeline_stage": "ingestion step 1",
        "some_other_key_maybe_airflow_run_id": "run 18",
    },
)
# </snippet>
# Constructing Validator by passing in RuntimeBatchRequest
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py get_validator">
my_validator: Validator = context.get_validator(
    batch_request=runtime_batch_request,
    expectation_suite=suite,  # OR
    # expectation_suite_name=suite_name
)
# </snippet>
my_validator.head()

# Constructing Validator by passing in arguments
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py get_validator_2">
my_validator: Validator = context.get_validator(
    datasource_name="my_spark_datasource",
    data_connector_name="my_runtime_data_connector",
    data_asset_name="insert_your_data_asset_name_here",
    runtime_parameters={"path": path_to_file},
    batch_identifiers={
        "some_key_maybe_pipeline_stage": "ingestion step 1",
        "some_other_key_maybe_airflow_run_id": "run 18",
    },
    batch_spec_passthrough={
        "reader_method": "csv",
        "reader_options": {"delimiter": ",", "header": True},
    },
    expectation_suite=suite,  # OR
    # expectation_suite_name=suite_name
)
# </snippet>
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py validator_head">
my_validator.head()
# </snippet>
