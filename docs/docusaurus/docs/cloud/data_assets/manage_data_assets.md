---
sidebar_label: 'Manage Data Assets'
title: 'Manage Data Assets'
description: Create and manage Data Assets in GX Cloud.
toc_min_heading_level: 2
toc_max_heading_level: 2
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

A Data Asset is a collection of records that you create when you connect to your Data Source. When you connect to your Data Source, you define a minimum of one Data Asset. You use these Data Assets to create the Batch Requests that select the data that is provided to your Expectations.

To learn more about Data Assets, see [Data Asset](/reference/learn/terms/data_asset.md).


## Create a Data Asset

Create a Data Asset to define the data you want GX Cloud to access. To connect to Data Assets for a Data Source not currently available in GX Cloud, see [Connect to a Data Source](/oss/guides/connecting_to_your_data/connect_to_data_lp.md) in the GX OSS documentation. 

<Tabs
  groupId="manage-data-assets"
  defaultValue='Snowflake'
  values={[
  {label: 'Snowflake', value:'Snowflake'},
  {label: 'PostgreSQL', value:'PostgreSQL'},
  ]}>
<TabItem value="Snowflake">

Define the data you want GX Cloud to access within Snowflake. 

### Prerequisites

- You have a [GX Cloud Beta account](https://greatexpectations.io/cloud).

- The GX Agent is running. See [Try GX Cloud](../try_gx_cloud.md) or [Connect GX Cloud](../connect/connect_lp.md).

- You have a Snowflake database, schema, and table.

- You have a [Snowflake account](https://docs.snowflake.com/en/user-guide-admin) with USAGE privileges on the table, database, and schema you are validating, and you have SELECT privileges on the table you are validating. To improve data security, GX recommends using a separate Snowflake user service account to connect to GX Cloud.

- You know your Snowflake password.

### Connect to a Snowflake Data Asset

1. In GX Cloud, click **Data Assets** > **New Data Asset**.

2. Click the **New Data Source** tab and then select **Snowflake**.

3. Enter a meaningful name for the Data Asset in the **Data Source name** field.

4. Optional. To use a connection string to connect to a Data Source, click the **Use connection string** selector, enter a connection string, and then move to step 6. 

5. Complete the following fields:

    - **Username**: Enter the username you use to access Snowflake.

    - **Account identifier**: Enter your Snowflake account or locator information. The locator value must include the geographical region. For example, `us-east-1`. To locate these values see [Account Identifiers](https://docs.snowflake.com/en/user-guide/admin-account-identifier).

    - **Password**: Enter a Snowflake password. To improve data security, GX recommends using a Snowflake service account to connect to GX Cloud.

    - **Database**: Enter the name of the Snowflake database where the data you want to validate is stored. In Snowsight, click **Data** > **Databases**. In the Snowflake Classic Console, click **Databases**.
 
    - **Schema**: Enter the name of the Snowflake schema (table) where the data you want to validate is stored.

    - **Warehouse**: Enter the name of your Snowflake database warehouse. In Snowsight, click **Admin** > **Warehouses**. In the Snowflake Classic Console, click **Warehouses**.

    - **Role**: Enter your Snowflake role.

6. Optional. Select **Test connection** to test the Data Source connection. Testing the connection to the Data Source is a preventative measure that makes sure the connection configuration is correct. This verification can help you avoid errors and can reduce troubleshooting downtime.

7. Click **Continue**.

8. Select **Table Asset** or **Query Asset** and complete the following fields:

    - **Table name**: When **Table Asset** is selected, enter a name for the table you're creating in the Data Asset.
    
    - **Data Asset name**: Enter a name for the Data Asset. Data Asset names must be unique. If you use the same name for multiple Data Assets, each Data Asset must be associated with a unique Data Source.

    - **Query**: When **Query Asset** is selected, enter the query that you want to run on the table. 

9. Select the **Complete Asset** tab to provide all Data Asset records to your Expectations and validations, or select the **Batches** tab to use subsets of Data Asset records for your Expectations and validations. If you selected the **Batches** tab, complete the following fields:

    - **Split Data Asset by** - Select **Year** to partition Data Asset records by year, select **Year - Month** to partition Data Asset records by year and month, or select **Year - Month - Day** to partition Data Asset records by year, month, and day.

    - **Column of datetime type** - Enter the name of the column containing the date and time data.

10. Optional. Select **Add Data Asset** to add additional tables or queries and repeat steps 8 and 9.

11. Click **Finish**.

12. Create an Expectation. See [Create an Expectation](/cloud/expectations/manage_expectations.md#create-an-expectation).

</TabItem>
<TabItem value="PostgreSQL">

Define the data you want GX Cloud to access within PostgreSQL.

### Prerequisites

- You have a [GX Cloud Beta account](https://greatexpectations.io/cloud).

- The GX Agent is running. See [Try GX Cloud](../try_gx_cloud.md) or [Connect GX Cloud](../connect/connect_lp.md).

- You have a PostgreSQL database, schema, and table.

- You have a [PostgreSQL instance](https://www.postgresql.org/download/). To improve data security, GX recommends using a separate user service account to connect to GX Cloud.

- You know your PostgreSQL access credentials.

### Connect to a PostgreSQL Data Asset 

1. In GX Cloud, click **Data Assets** > **New Data Asset**.

2. Click the **New Data Source** tab and then select **PostgreSQL**.

3. Enter a meaningful name for the Data Asset in the **Data Source name** field.

4. Enter a connection string in the **Connection string** field. The connection string format is `postgresql+psycopg2//YourUserName:YourPassword@YourHostname:5432/YourDatabaseName`. 

5. Optional. Select **Test connection** to test the Data Source connection. Testing the connection to the Data Source is a preventative measure that makes sure the connection configuration is correct. This verification can help you avoid errors and can reduce troubleshooting downtime.

6. Click **Continue**.

7. Select **Table Asset** or **Query Asset** and complete the following fields:

    - **Table name**: When **Table Asset** is selected, enter a name for the table you're creating in the Data Asset.
    
    - **Data Asset name**: Enter a name for the Data Asset. Data Asset names must be unique across all Data Sources in GX Cloud.

    - **Query**: When **Query Asset** is selected, enter the query that you want to run on the table. 

8. Select the **Complete Asset** tab to provide all Data Asset records to your Expectations and validations, or select the **Batches** tab to use subsets of Data Asset records for your Expectations and validations. If you selected the **Batches** tab, complete the following fields:

    - **Split Data Asset by** - Select **Year** to partition Data Asset records by year, select **Year - Month** to partition Data Asset records by year and month, or select **Year - Month - Day** to partition Data Asset records by year, month, and day.

    - **Column of datetime type** - Enter the name of the column containing the date and time data.

9. Optional. Select **Add Data Asset** to add additional tables or queries and repeat steps 8 and 9.

10. Click **Finish**.

11. Create an Expectation. See [Create an Expectation](/cloud/expectations/manage_expectations.md#create-an-expectation).

</TabItem>
</Tabs>


## View Data Asset metrics

Data Asset metrics provide you with insight into the data you can use for your data validations. 

1. In GX Cloud, click **Data Assets** and then select a Data Asset in the **Data Assets** list.

2. Click the **Overview** tab.

3. Select one of the following options: 

    - If you have not previously generated Data Asset metrics, click **Fetch Metrics**. 

    - If you previously generated Data Asset metrics, click **Refresh** to refresh the metrics.

### Available Data Asset metrics

The following table lists the available Data Asset metrics.

| Column                                   | Description                                               | 
|------------------------------------------|-----------------------------------------------------------|
| **Row Count**                            | The number of rows within a Data Asset.                   | 
| **Column**                               | A column within your Data Asset.                          | 
| **Type**                                 | The data storage type in the Data Asset column.           | 
| **Min**                                  | For numeric columns the lowest value in the column.       | 
| **Max**                                  | For numeric columns, the highest value in the column.     | 
| **Mean**                                 | For numeric columns, the average value with the column.<br/> This is determined by dividing the sum of all values in the Data Asset by the number of values.  |
| **Median**                                 | For numeric columns, the value in the middle of a data set.<br/> 50% of the data within the Data Asset has a value smaller or equal to the median, and 50% of the data within the Data Asset has a value that is higher or equal to the median.  |
| **Null %**                                | The percentage of missing values in a column.             |

## Add an Expectation to a Data Asset column

When you create an Expectation after fetching metrics for a Data Asset, the column names and some values are autopopulated for you and this can simplify the creation of new Expectations. Data Asset Metrics can also help you determine what Expectations might be useful and how they should be configured. When you create new Expectations after fetching Data Asset Metrics, you can add them to an existing Expectation Suite, or you can create a new Expectation Suite and add the Expectations to it. 

1. In GX Cloud, click **Data Assets** and then select a Data Asset in the **Data Assets** list.

2. Click the **Overview** tab.

3. Select one of the following options: 

    - If you have not previously generated Data Asset metrics, click **Fetch Metrics**. 

    - If you previously generated Data Asset metrics, click **Refresh** to refresh the metrics.

4. Click **New Expectation**.

5. Select one of the following options:

    - To add an Expectation to a new Expectation Suite, click the **New Suite** tab and then enter a name for the new Expectation Suite.

    - To add an Expectation to an existing Expectation Suite, click the **Existing Suite** tab and then select an existing Expectation Suite.

6. Select an Expectation type. See [Available Expectation types](/cloud/expectations/manage_expectations.md#available-expectation-types).

7. Complete the fields in the **Create Expectation** pane.

8. Click **Save** to add the Expectation, or click **Save & Add More** to add additional Expectations.


## Add a Data Asset to an Existing Data Source

Additional Data Assets can only be added to Data Sources created in GX Cloud.

1. In GX Cloud, click **Data Assets** and then select **New Data Asset**.

2. Click the **Existing Data Source** tab and then select a Data Source.

3. Click **Add Data Asset**.

4. Select **Table Asset** or **Query Asset** and complete the following fields:

    - **Table name**: When **Table Asset** is selected, enter a name for the table you're creating in the Data Asset.

    - **Query**: When **Query Asset** is selected, enter the query that you want to run on the table. 

    - **Data Asset name**: Enter a name for the Data Asset. Data Asset names must be unique. If you use the same name for multiple Data Assets, each Data Asset must be associated with a unique Data Source.

5. Select the **Complete Asset** tab to provide all Data Asset records to your Expectations and validations, or select the **Batches** tab to use subsets of Data Asset records for your Expectations and validations. If you selected the **Batches** tab, complete the following fields:

    - **Split Data Asset by** - Select **Year** to partition Data Asset records by year, select **Year - Month** to partition Data Asset records by year and month, or select **Year - Month - Day** to partition Data Asset records by year, month, and day.

    - **Column of datetime type** - Enter the name of the column containing the date and time data.

6. Optional. Select **Add Data Asset** to add additional tables or queries and repeat step 4.

7. Click **Finish**.


## Edit Data Source settings

Edit Data Source settings to update Data Source connection information or access credentials. You can only edit the settings of Data Sources created in GX Cloud.

<Tabs
  groupId="manage-data-assets"
  defaultValue='Snowflake'
  values={[
  {label: 'Snowflake', value:'Snowflake'},
  {label: 'PostgreSQL', value:'PostgreSQL'},
  ]}>
<TabItem value="Snowflake">

1. In GX Cloud, click **Data Assets**.

2. Click **Manage Data Sources**.

3. Click **Edit Data Source** for the Snowflake Data Source you want to edit.

4. Optional. Edit the Data Source name.

5. Optional. If you used a connection string to connect to the Data Source, click the **Use connection string** slider and edit the Data Source connection string.

6. Optional. If you're not using a connection string, edit the following fields:
    
     - **Username**: Enter a new Snowflake username.

    - **Account identifier**: Enter new Snowflake account or locator information. The locator value must include the geographical region. For example, `us-east-1`. To locate these values see [Account Identifiers](https://docs.snowflake.com/en/user-guide/admin-account-identifier).

    - **Password**: Enter the password for the Snowflake user you're connecting to GX Cloud. To improve data security, GX recommends using a Snowflake service account to connect to GX Cloud.

    - **Database**: Enter a new Snowflake database name.
 
    - **Schema**: Enter a new schema name.

    - **Warehouse**: Enter a new Snowflake database warehouse name.

    - **Role**: Enter a new Snowflake role.

7. Click **Save**.

</TabItem>
<TabItem value="PostgreSQL">

1. In GX Cloud, click **Data Assets**.

2. Click **Manage Data Sources**.

3. Click **Edit Data Source** for the PostgreSQL Data Source you want to edit.

4. Optional. Edit the Data Source name.

5. Optional. Click **Show** in the **Connection string** field and then edit the Data Source connection string.

6. Click **Save**.


</TabItem>
</Tabs>

## Edit a Data Asset

You can only edit the settings of Data Assets created in GX Cloud.

1. In GX Cloud, click **Data Assets** and in the Data Assets list click **Edit Data Asset** for the Data Asset you want to edit.

2. Edit the following fields:

    - **Table name**: Enter a new name for the Data Asset table.

    - **Data Asset name**: Enter a new name for the Data Asset. If you use the same name for multiple Data Assets, each Data Asset must be associated with a unique Data Source.

3. Click **Save**.

## Secure your GX API Data Source connection strings

When you use the GX API and not GX Cloud to connect to Data Sources, you can obfuscate sensitive Data Source credentials in your connection string as an additional security measure.

1. Store your credential value as an environment variable by entering `export ENV_VAR_NAME=env_var_value` in the terminal or adding the command to your `~/.bashrc` or `~/.zshrc` file. For example:

    ```bash title="Terminal input"
    export GX_CLOUD_SNOWFLAKE_PASSWORD=<password-string>
    ```
    Prefix environment variable names with `GX_CLOUD_`.

2. Create a Data Source connection string using the environment variable name instead of the credential value. For example:

    ```python title="Example Data Source connection string"
    snowflake://<user-name>:${GX_CLOUD_SNOWFLAKE_PASSWORD}@<account-name>/<database-name>/<schema-name>?warehouse=<warehouse-name>&role=<role-name>
    ```
    Environment variable names must be enclosed by curly braces and be preceded by a dollar sign. For example: `${GX_CLOUD_SNOWFLAKE_PASSWORD}`. Do not use interpolation to add credential values to connection strings.

3. Use the environment variable to supply the credential value when you run the GX Agent. For example:

    ```bash title="Terminal input"
    docker run --rm -e GX_CLOUD_SNOWFLAKE_PASSWORD="<snowflake_password>" -e GX_CLOUD_ACCESS_TOKEN="<user_access_token>" -e GX_CLOUD_ORGANIZATION_ID="<organization_id>" greatexpectations/agent
    ```

## Delete a Data Asset

1. In GX Cloud, click **Settings** > **Datasources**.

2. Click **Delete** for the Data Source and the associated Data Assets you want to delete.

3. Click **Delete**.

