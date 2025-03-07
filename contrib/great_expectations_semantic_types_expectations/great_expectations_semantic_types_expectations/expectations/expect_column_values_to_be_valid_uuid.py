"""
This is a template for creating custom ColumnMapExpectations.
For detailed instructions on how to use it, please see:
    https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/how_to_create_custom_column_map_expectations
"""

from uuid import UUID

from great_expectations.execution_engine import (
    PandasExecutionEngine,
    SqlAlchemyExecutionEngine,
)
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import (
    ColumnMapMetricProvider,
    column_condition_partial,
)


def is_valid_uuid(uuid: str) -> bool:
    try:
        UUID(uuid)
        return True
    except ValueError:
        return False


# This class defines a Metric to support your Expectation.
# For most ColumnMapExpectations, the main business logic for calculation will live in this class.
class ColumnValuesToBeValidUUID(ColumnMapMetricProvider):
    # This is the id string that will be used to reference your metric.
    condition_metric_name = "column_values.valid_uuid"

    # This method implements the core logic for the PandasExecutionEngine
    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        return column.apply(lambda x: is_valid_uuid(x))

    # This method defines the business logic for evaluating your metric when using a SqlAlchemyExecutionEngine
    @column_condition_partial(engine=SqlAlchemyExecutionEngine)
    def _sqlalchemy(cls, column, _dialect, **kwargs):
        """
        Please note that there is a stricter version to verify GUID, as can be seen in the following link:
        https://www.techtarget.com/searchwindowsserver/definition/GUID-global-unique-identifier#:~:text=RFC%204122%20specification.-,How%20does%20GUID%20work%3F,-GUIDs%20are%20constructed
        However, since the UUID package doesn't seem to enforce it, the chosen regex was the less stricter.
        For future purposes, the stricter pattern can be found here as well, commented out.
        """
        # regex_pattern = '^(urn:uuid:)?\{?[A-Fa-f0-9]{8}-?[A-Fa-f0-9]{4}-?[1-5][A-Fa-f0-9]{3}-?[89ABab][A-Fa-f0-9]{3}-?[A-Fa-f0-9]{12}\}?$'
        regex_pattern = (
            "^(urn:uuid:)?\\{?[0-9a-fA-F]{8}(-?[0-9a-fA-F]{4}){3}-?[0-9a-fA-F]{12}\\}?$"
        )
        return column.regexp_match(regex_pattern)

    # This method defines the business logic for evaluating your metric when using a SparkDFExecutionEngine
    # @column_condition_partial(engine=SparkDFExecutionEngine)
    # def _spark(cls, column, **kwargs):
    #     raise NotImplementedError


# This class defines the Expectation itself
class ExpectColumnValuesToBeValidUUID(ColumnMapExpectation):
    """Expect column values to conform to valid UUID format."""

    # These examples will be shown in the public gallery.
    # They will also be executed as unit tests for your Expectation.
    examples = [
        {
            "data": {
                "well_formed_uuids": [
                    # standard random UUIDs
                    "28d12e8e-80aa-4b32-8afb-19da0aa7e3d5",
                    "d711cb07-1f05-4ef6-bc54-3a5ec703a88d",
                    "9d5175ae-4d9e-4370-854c-a5e9bbb9b2c7",
                    "c3eef74b-d977-46e3-ad40-0bfe5dbaf64b",
                    # hyphens may or may not be present
                    "e8a4926e5f7643079e8acdbd49a4e15b",
                    # curly braces may or may not be present
                    "{00010203-0405-1607-8809-0a0b0c0d0e0f}",
                    # leading identifier "urn:uuid:" is allowed
                    "urn:uuid:12345678-1234-5678-9234-567812345678",
                ],
                "malformed_uuids": [
                    # has non-hexidecimal value
                    "5d700619-51de-4e28-b949-f596cddcd25z",
                    # is too long
                    "ff4a6854-79b9-4210-82b3-ca7cd6d03b711",
                    # is too short
                    "19bf8112-a972-4e38-a404-16864cb9d88",
                    # has invalid punctuation
                    "f13cbe4c_05df_4cbf_88f6_3b8c7d2f5cfc",
                    # more invalid punctuation
                    "a82af99c.20d3.4bb4.9a73.b9ec7c6f6a36",
                    # left field
                    "not-even-close",
                    "ValueError('All arrays must be of the same length')",
                ],
            },
            "tests": [
                {
                    "title": "basic_positive_test",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "well_formed_uuids"},
                    "out": {"success": True},
                },
                {
                    "title": "basic_negative_test",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "malformed_uuids"},
                    "out": {"success": False},
                },
            ],
        }
    ]

    # This is the id string of the Metric used by this Expectation.
    # For most Expectations, it will be the same as the `condition_metric_name` defined in your Metric class above.
    map_metric = "column_values.valid_uuid"

    # This is a list of parameter names that can affect whether the Expectation evaluates to True or False
    success_keys = ("mostly",)

    # This dictionary contains default values for any parameters that should have default values
    default_kwarg_values = {}

    # This object contains metadata for display in the public Gallery
    library_metadata = {
        "tags": ["typed-entities"],  # Tags for this Expectation in the Gallery
        "contributors": [  # Github handles for all contributors to this Expectation.
            "@joshua-stauffer",  # Don't forget to add your github handle here!
            "@asafla",
        ],
    }


if __name__ == "__main__":
    ExpectColumnValuesToBeValidUUID().print_diagnostic_checklist()
