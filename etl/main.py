from data_loader import data_loader
import yaml
import pandas as pd
from logger import logger


def split_data(df):
    """
    Perform data splitting to prepare fact and dimension tables.

    Parameters:
    df (DataFrame): Input DataFrame containing raw data.

    Returns:
    tuple: A tuple containing dimension tables and the fact table.
    """
    try:
        logger.info("Starting transformation stage...")
        logger.debug(f"Number of duplicate rows: {df.duplicated().sum()}")

        # Convert column data type
        df['Purchase Amount (USD)'] = df['Purchase Amount (USD)'].astype(float)

        # Split into Fact and Dimension Tables
        dim_customer = df[['Customer ID', 'Age', 'Gender', 'Subscription Status',
                           'Frequency of Purchases', 'Previous Purchases']].drop_duplicates()

        dim_product = df[['Item Purchased', 'Category', 'Size', 'Color', 'Season']].drop_duplicates()
        dim_product['Product ID'] = range(1, len(dim_product) + 1)

        dim_loc = df[['Location']].drop_duplicates()
        dim_loc['Location ID'] = range(1, len(dim_location) + 1)

        dim_payment = df[['Payment Method', 'Preferred Payment Method']].drop_duplicates()
        dim_payment['Payment Method ID'] = range(1, len(dim_payment) + 1)

        fact_purchases = (
            df.merge(dim_product, on=['Item Purchased', 'Category', 'Size', 'Color', 'Season'], how='left')
            .merge(dim_loc, on=['Location'], how='left')
            .merge(dim_payment, on=['Payment Method', 'Preferred Payment Method'], how='left')
        )
        fact_purchases = fact_purchases[['Customer ID', 'Product ID', 'Location ID', 'Payment Method ID',
                                         'Purchase Amount (USD)', 'Review Rating', 'Shipping Type',
                                         'Discount Applied', 'Promo Code Used']]

        logger.info("Transformation stage completed successfully.")
        return (dim_customer, dim_product, dim_loc, dim_payment), fact_purchases

    except Exception as e:
        logger.error("Data transformation failed.", exc_info=True)
        raise


def extract(file_path):
    """
    Extract data from a CSV file.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    DataFrame: Extracted DataFrame.
    """
    try:
        logger.info(f"Extracting data from: {file_path}")
        df = pd.read_csv(file_path)
        logger.debug(f"Data sample:\n{df.head()}")
        logger.debug(f"DataFrame info:\n{df.info()}")
        logger.info(f"Successfully extracted {len(df)} rows.")
        return df

    except Exception as e:
        logger.error("Failed to extract data.", exc_info=True)
        raise


def main():
    """
    Main function to execute the ETL pipeline.
    """
    try:
        logger.info("Starting the ETL pipeline...")

        # Load configuration
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)

        # Extract data
        data = extract('/Users/reemassi/PycharmProjects/course/data.csv')

        # Transform data
        dim_tables, fact_table = split_data(data)

        # Load data
        data_loader(dim_tables, fact_table, config["database"])

        logger.info("ETL pipeline completed successfully.")

    except Exception as e:
        logger.error("ETL pipeline failed.", exc_info=True)
        raise


if __name__ == "__main__":
    main()
