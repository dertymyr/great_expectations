---
title: Create and edit Expectations based on domain knowledge, without inspecting data directly
tag: [how-to, getting started]
description: Create ExpectationConfigurations based on domain knowledge.
keywords: [Expectations, Domain Knowledge]
---

import Prerequisites from '../../components/_prerequisites.jsx'
import PrerequisiteQuickstartGuideComplete from '../../components/prerequisites/_quickstart_completed.mdx'
import TechnicalTag from '../../term_tags/_tag.mdx';
import IfYouStillNeedToSetupGX from '../../components/prerequisites/_if_you_still_need_to_setup_gx.md'
import DataContextInitializeQuickOrFilesystem from '../../components/setup/link_lists/_data_context_initialize_quick_or_filesystem.mdx'
import ConnectingToDataFluently from '../../components/connect_to_data/link_lists/_connecting_to_data_fluently.md'

This guide shows how to create an <TechnicalTag tag="expectation_suite" text="Expectation Suite" /> without a sample <TechnicalTag tag="batch" text="Batch" />.

The following are the reasons why you might want to do this:

- You don't have a sample.
- You don't currently have access to the data to make a sample.
- You know exactly how you want your <TechnicalTag tag="expectation" text="Expectations" /> to be configured.
- You want to create Expectations parametrically (you can also do this in interactive mode).
- You don't want to spend the time to validate against a sample.

If you have a use case we have not considered, please [contact us on Slack](https://greatexpectations.io/slack).

:::info Does this process edit my data?
No.  The interactive method used to create and edit Expectations does not edit or alter the Batch data.
:::


## Prerequisites

<Prerequisites>

- Great Expectations installed in a Python environment
- A Filesystem Data Context for your Expectations
- Created a Data Source from which to request a Batch of data for introspection

</Prerequisites>

## Import the Great Expectations module and instantiate a Data Context

For this guide we will be working with Python code in a Jupyter Notebook. Jupyter is included with GX and lets us easily edit code and immediately see the results of our changes.

Run the following code to import Great Expectations and instantiate a Data Context:

```python name="version-0.17.23 docs/docusaurus/versioned_docs/version-0.17.23/guides/expectations/how_to_create_and_edit_an_expectationsuite_domain_knowledge.py get_data_context"
```

:::info Data Contexts and persisting data

If you're using an Ephemeral Data Context, your configurations will not persist beyond the current Python session.  However, if you're using a Filesystem or Cloud Data Context, they do persist.  The `get_context()` method returns the first Cloud or Filesystem Data Context it can find.  If a Cloud or Filesystem Data Context has not be configured or cannot be found, it provides an Ephemeral Data Context.  For more information about the `get_context()` method, see [Instantiate a Data Context](/guides/setup/configuring_data_contexts/instantiating_data_contexts/instantiate_data_context.md).

:::

## Create an ExpectationSuite 

We will use the `add_expectation_suite()` method to create an empty ExpectationSuite.

```python name="version-0.17.23 docs/docusaurus/versioned_docs/version-0.17.23/guides/expectations/how_to_create_and_edit_an_expectationsuite_domain_knowledge.py create_expectation_suite"
```

## Create Expectation Configurations

You are adding Expectation configurations to the suite. Since there is no sample Batch of data, no <TechnicalTag tag="validation" text="Validation" /> happens during this process. To illustrate how to do this, consider a hypothetical example. Suppose that you have a table with the columns ``account_id``, ``user_id``, ``transaction_id``, ``transaction_type``, and ``transaction_amt_usd``. Then the following code snipped adds an Expectation that the columns of the actual table will appear in the order specified above:

```python name="version-0.17.23 docs/docusaurus/versioned_docs/version-0.17.23/guides/expectations/how_to_create_and_edit_an_expectationsuite_domain_knowledge.py create_expectation_1"
```

Here are a few more example expectations for this dataset:


```python name="version-0.17.23 docs/docusaurus/versioned_docs/version-0.17.23/guides/expectations/how_to_create_and_edit_an_expectationsuite_domain_knowledge.py create_expectation_2"
```

```python name="version-0.17.23 docs/docusaurus/versioned_docs/version-0.17.23/guides/expectations/how_to_create_and_edit_an_expectationsuite_domain_knowledge.py create_expectation_3"
```

```python name="version-0.17.23 docs/docusaurus/versioned_docs/version-0.17.23/guides/expectations/how_to_create_and_edit_an_expectationsuite_domain_knowledge.py create_expectation_4"
```

You can see all the available Expectations in the [Expectation Gallery](https://greatexpectations.io/expectations).

## Save your Expectations for future use

To keep your Expectations for future use, you save them to your Data Context.  A Filesystem or Cloud Data Context persists outside the current Python session, so saving the Expectation Suite in your Data Context's Expectations Store ensures you can access it in the future:

```python name="version-0.17.23 docs/docusaurus/versioned_docs/version-0.17.23/guides/expectations/how_to_create_and_edit_an_expectationsuite_domain_knowledge.py save_expectation_suite"
```

:::caution Ephemeral Data Contexts and persistence

Ephemeral Data Contexts don't persist beyond the current Python session.  If you're working with an Ephemeral Data Context, you'll need to convert it to a Filesystem Data Context using the Data Context's `convert_to_file_context()` method.  Otherwise, your saved configurations won't be available in future Python sessions as the Data Context itself is no longer available.

:::

## Next steps

Now that you have created and saved an Expectation Suite, you can [Validate your data](/guides/validation/validate_data_overview.md).