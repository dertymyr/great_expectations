---
title: Use Great Expectations with Amazon Web Services using Redshift
sidebar_label: "AWS S3 and Redshift"
---
import Prerequisites from '../../components/_prerequisites.jsx'
import PrereqPython from '../../components/prerequisites/_python_version.md'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Congratulations from './components/_congratulations_aws_redshift.md'
import TechnicalTag from '../../term_tags/_tag.mdx';

<!-- Part 1: Setup -->

<!-- 1.1 Ensure that the AWS CLI is ready for use -->

<!-- 1.1.1 Verify that the AWS CLI is installed -->
import VerifyAwsInstalled from './components/_aws_cli_verify_installation.md'

<!-- 1.1.2 Verify that your AWS credentials are properly configured -->
import VerifyAwsCredentials from '../../guides/setup/configuring_metadata_stores/components/_verify_aws_credentials_are_configured_properly.mdx'

<!-- 1.2 Prepare a local installation of Great Expectations -->

<!-- 1.2.1 Verify that your Python version meets requirements -->

import VerifyPythonVersion from '../../guides/setup/installation/components_local/_check_python_version.mdx'
import WhereToGetPython from './components/_python_where_to_get.md'

<!-- 1.2.2 Create a virtual environment for your Great Expectations project -->

import CreateVirtualEnvironment from '../../guides/setup/installation/components_local/_create_an_venv_with_pip.mdx'

<!-- 1.2.3 Ensure you have the latest version of pip -->

import GetLatestPip from '../../guides/setup/installation/components_local/_ensure_latest_pip.mdx'

<!-- 1.2.4 Install boto3 -->

import InstallBoto3WithPip from '../../guides/setup/configuring_metadata_stores/components/_install_boto3_with_pip.mdx'


<!-- 1.2.5 Install Great Expectations -->

import InstallGxWithPip from '../../guides/setup/installation/components_local/_install_ge_with_pip.mdx'

<!-- 1.2.6 Verify that Great Expectations installed successfully -->

import VerifySuccessfulGxInstallation from '../../guides/setup/installation/components_local/_verify_ge_install_succeeded.mdx'


<!-- 1.2.7 Install dependencies for Redshift -->
import RedshiftDependencies from '../../guides/connecting_to_your_data/database/components/_redshift_dependencies.md'

<!-- 1.3 Create your Data Context -->

import CreateDataContextWithCreate from './components/_initialize_data_context_with_create.mdx'

<!-- 1.4 Configure your Expectations Store on Amazon S3 -->

<!-- 1.4.1 Identify your Data Context Expectations Store -->

import IdentifyDataContextExpectationsStore from '../../guides/setup/configuring_metadata_stores/components_how_to_configure_an_expectation_store_in_amazon_s3/_identify_your_data_context_expectations_store.mdx'

<!-- 1.4.2 Update your configuration file to include a new Store for Expectations on Amazon S3 -->

import AddS3ExpectationsStoreConfiguration from '../../guides/setup/configuring_metadata_stores/components_how_to_configure_an_expectation_store_in_amazon_s3/_update_your_configuration_file_to_include_a_new_store_for_expectations_on_s.mdx'

<!-- 1.4.3 (Optional) Copy existing Expectation JSON files to the Amazon S3 bucket -->

import OptionalCopyExistingExpectationsToS3 from '../../guides/setup/configuring_metadata_stores/components_how_to_configure_an_expectation_store_in_amazon_s3/_copy_existing_expectation_json_files_to_the_s_bucket_this_step_is_optional.mdx'

<!-- 1.4.4 (Optional) Verify that copied Expectations can be accessed from Amazon S3 -->

import OptionalVerifyCopiedExpectationsAreAccessible from '../../guides/setup/configuring_metadata_stores/components_how_to_configure_an_expectation_store_in_amazon_s3/_confirm_list.mdx'

<!-- 1.5 Configure your Validation Results Store on Amazon S3 -->

<!-- 1.5.1 Identify your Data Context's Validation Results Store -->

import IdentifyDataContextValidationResultsStore from '../../guides/setup/configuring_metadata_stores/components_how_to_configure_a_validation_result_store_in_amazon_s3/_identify_your_data_context_validation_results_store.mdx'

<!-- 1.5.2 Update your configuration file to include a new Store for Validation Results on Amazon S3 -->

import AddS3ValidationResultsStoreConfiguration from '../../guides/setup/configuring_metadata_stores/components_how_to_configure_a_validation_result_store_in_amazon_s3/_update_your_configuration_file_to_include_a_new_store_for_validation_results_on_s.mdx'

<!-- 1.5.3 (Optional) Copy existing Validation results to the Amazon S3 bucket -->

import OptionalCopyExistingValidationResultsToS3 from '../../guides/setup/configuring_metadata_stores/components_how_to_configure_a_validation_result_store_in_amazon_s3/_copy_existing_validation_results_to_the_s_bucket_this_step_is_optional.mdx'

<!-- 1.6 Configure Data Docs for hosting and sharing from Amazon S3 -->

<!-- 1.6.1 Create an Amazon S3 bucket for your Data Docs -->
import CreateAnS3BucketForDataDocs from '../../guides/setup/configuring_data_docs/components_how_to_host_and_share_data_docs_on_amazon_s3/_create_an_s3_bucket.mdx'

<!-- 1.6.2 Configure your bucket policy to enable appropriate access -->
import ConfigureYourBucketPolicyToEnableAppropriateAccess from '../../guides/setup/configuring_data_docs/components_how_to_host_and_share_data_docs_on_amazon_s3/_configure_your_bucket_policy_to_enable_appropriate_access.mdx'

<!-- 1.6.3 Apply the access policy to your Data Docs' Amazon S3 bucket -->
import ApplyTheDataDocsAccessPolicy from '../../guides/setup/configuring_data_docs/components_how_to_host_and_share_data_docs_on_amazon_s3/_apply_the_policy.mdx'

<!-- 1.6.4 Add a new Amazon S3 site to the `data_docs_sites` section of your `great_expectations.yml` -->
import AddANewS3SiteToTheDataDocsSitesSectionOfYourGreatExpectationsYml from '../../guides/setup/configuring_data_docs/components_how_to_host_and_share_data_docs_on_amazon_s3/_add_a_new_s3_site_to_the_data_docs_sites_section_of_your_great_expectationsyml.mdx'

<!-- 1.6.5 Test that your Data Docs configuration is correct by building the site -->
import TestThatYourConfigurationIsCorrectByBuildingTheSite from '../../guides/setup/configuring_data_docs/components_how_to_host_and_share_data_docs_on_amazon_s3/_test_that_your_configuration_is_correct_by_building_the_site.mdx'

<!-- Additional notes on hosting Data Docs from an Amazon S3 bucket -->
import AdditionalDataDocsNotes from '../../guides/setup/configuring_data_docs/components_how_to_host_and_share_data_docs_on_amazon_s3/_additional_notes.mdx'

<!-- Part 2: Connect to data -->

<!-- 2.1 Instantiate your project's Data Context -->

import CreateDataContextWithCreateAgain from './components/_initialize_data_context_with_create.mdx'

<!-- 2.1.1 Determine your connection string -->

import ConnectionStringRedshift from '../../guides/connecting_to_your_data/database/components/_redshift_credentials.md'

<!-- 2.2 Add Data Source to your DataContext -->

import ConfigureYourRedshiftDatasource from './components/_configure_your_redshift_datasource.mdx'

<!-- 2.3. Connect to a specific set of data with a Data Asset -->

import ConnectToDataAssets from './components/_add_table_and_query_assets.mdx'

<!-- 2.4 Test your new Data Source -->

import TestRedshiftDatasource from './components/_test_your_new_redshift_datasource.mdx'

<!-- Part 3: Create Expectations -->

<!-- 3.1 Prepare a Batch Request-->

import PrepareABatchRequestAndValidatorForCreatingExpectations from './components/_add_expectation_suite_and_validator_for_fluent_datasource.mdx'

<!-- 3.2: Use a Validator to add Expectations to the Expectation Suite -->

import CreateExpectationsInteractively from './components/_expectation_suite_add_expectations_with_validator.md'

<!-- 3.3 Save the Expectation Suite -->

import SaveTheExpectationSuite from './components/_expectation_suite_save.md'

<!-- Part 4: Validate Data -->

<!-- 4.1 Create and run a Checkpoint -->

import CheckpointCreateAndRun from './components/_checkpoint_create_and_run.md'

<!-- 4.1.1 Create a Checkpoint -->

import CreateCheckpoint from './components/_checkpoint_create.md'

<!-- 4.1.2 Run the Checkpoint -->

import RunCheckpoint from './components/_checkpoint_run.md'

<!-- 4.2 Build and view Data Docs -->
import BuildAndViewDataDocs from './components/_data_docs_build_and_view.md'

Great Expectations can work within many frameworks.  In this guide you will be shown a workflow for using Great Expectations with AWS and cloud storage.  You will configure a local Great Expectations project to store Expectations, Validation Results, and Data Docs in Amazon S3 buckets.  You will further configure Great Expectations to access data from a Redshift database.

This guide will demonstrate each of the steps necessary to go from installing a new instance of Great Expectations to Validating your data for the first time and viewing your Validation Results as Data Docs.

## Prerequisites

<Prerequisites>

- <PrereqPython />
- The AWS CLI. To download and install the AWS CLI, see [Installing or updating the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
- AWS credentials. See [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
- Permissions to install the Python packages ([`boto3`](https://github.com/boto/boto3) and `great_expectations`) with pip.
- An S3 bucket and prefix to store Expectations and Validation Results.

</Prerequisites>

## Steps

## Part 1: Setup

### 1.1 Ensure that the AWS CLI is ready for use

#### 1.1.1 Verify that the AWS CLI is installed
<VerifyAwsInstalled />

#### 1.1.2 Verify that your AWS credentials are properly configured
<VerifyAwsCredentials />

### 1.2 Prepare a local installation of Great Expectations

#### 1.2.1 Verify that your Python version meets requirements
<VerifyPythonVersion />

<WhereToGetPython />

#### 1.2.2 Create a virtual environment for your Great Expectations project
<CreateVirtualEnvironment />

#### 1.2.3 Ensure you have the latest version of pip
<GetLatestPip />

#### 1.2.4 Install boto3
<InstallBoto3WithPip />

#### 1.2.5 Install Great Expectations
<InstallGxWithPip />

#### 1.2.6 Verify that Great Expectations installed successfully
<VerifySuccessfulGxInstallation />

#### 1.2.7 Install additional dependencies for Redshift

<RedshiftDependencies />

### 1.3 Create your Data Context
<CreateDataContextWithCreate />

### 1.4 Configure your Expectations Store on Amazon S3

#### 1.4.1 Identify your Data Context Expectations Store
<IdentifyDataContextExpectationsStore />

#### 1.4.2 Update your configuration file to include a new Store for Expectations on Amazon S3
<AddS3ExpectationsStoreConfiguration />

#### 1.4.3 (Optional) Copy existing Expectation JSON files to the Amazon S3 bucket
<OptionalCopyExistingExpectationsToS3 />

#### 1.4.4 (Optional) Verify that copied Expectations can be accessed from Amazon S3
<OptionalVerifyCopiedExpectationsAreAccessible />

### 1.5 Configure your Validation Results Store on Amazon S3

#### 1.5.1 Identify your Data Context's Validation Results Store
<IdentifyDataContextValidationResultsStore />

#### 1.5.2 Update your configuration file to include a new Store for Validation Results on Amazon S3
<AddS3ValidationResultsStoreConfiguration />

#### 1.5.3 (Optional) Copy existing Validation results to the Amazon S3 bucket
<OptionalCopyExistingValidationResultsToS3 />

### 1.6 Configure Data Docs for hosting and sharing from Amazon S3

#### 1.6.1 Create an Amazon S3 bucket for your Data Docs
<CreateAnS3BucketForDataDocs />

#### 1.6.2 Configure your bucket policy to enable appropriate access
<ConfigureYourBucketPolicyToEnableAppropriateAccess />

#### 1.6.3 Apply the access policy to your Data Docs' Amazon S3 bucket
<ApplyTheDataDocsAccessPolicy />

#### 1.6.4 Add a new Amazon S3 site to the `data_docs_sites` section of your `great_expectations.yml`
<AddANewS3SiteToTheDataDocsSitesSectionOfYourGreatExpectationsYml />

#### 1.6.5 Test that your Data Docs configuration is correct by building the site
<TestThatYourConfigurationIsCorrectByBuildingTheSite />

#### Additional notes on hosting Data Docs from an Amazon S3 bucket
<AdditionalDataDocsNotes />

## Part 2: Connect to data

### 2.1 Instantiate your project's DataContext
<CreateDataContextWithCreateAgain />

If you have already instantiated your `DataContext` in a previous step, this step can be skipped.

#### 2.1.1 Determine your connection string

<ConnectionStringRedshift />

:::tip Is there a more secure way to store my credentials than plain text in a connection string?

We recommend that database credentials be stored in the `config_variables.yml` file, which is located in the `uncommitted/` folder by default, and is not part of source control.

For additional options on configuring the `config_variables.yml` file or additional environment variables, please see our guide on [how to configure credentials](/guides/setup/configuring_data_contexts/how_to_configure_credentials.md).

:::

### 2.2 Add Data Source to your DataContext
<ConfigureYourRedshiftDatasource />

### 2.3. Connect to a specific set of data with a Data Asset
<ConnectToDataAssets />

### 2.4 Test your new Data Source
<TestRedshiftDatasource />

## Part 3: Create Expectations

### 3.1: Prepare a Batch Request, empty Expectation Suite, and Validator

<PrepareABatchRequestAndValidatorForCreatingExpectations />

### 3.2: Use a Validator to add Expectations to the Expectation Suite

<CreateExpectationsInteractively />

### 3.3: Save the Expectation Suite

<SaveTheExpectationSuite />

## Part 4: Validate Data

### 4.1: Create and run a Checkpoint

<CheckpointCreateAndRun />

#### 4.1.1 Create a Checkpoint

<CreateCheckpoint />

#### 4.1.2 Run the Checkpoint

<RunCheckpoint />

### 4.2: Build and view Data Docs

<BuildAndViewDataDocs />
