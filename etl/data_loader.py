from sqlalchemy import create_engine
from logger import logger


def data_loader(dim_tables, fact_table, config):
    """
    Load data into a PostgreSQL database.

    Parameters:
    dim_tables (tuple): Tuple containing dataframes for dimension tables.
    fact_table (DataFrame): Dataframe for the fact table.
    config (dict): Configuration dictionary with database connection parameters.

    """
    logger.info("Initializing data loading process into the database...")

    try:
        # Establish database connection
        engine = create_engine(
            f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        )

        # Unpack and load dimension tables
        table_names = ['dim_customer', 'dim_product', 'dim_location', 'dim_payment_method']
        for table_name, dim_table in zip(table_names, dim_tables):
            dim_table.to_sql(table_name, con=engine, index=False, if_exists='replace')
            logger.info(f"Loaded dimension table: {table_name}")

        # Load fact table
        fact_table_name = 'fact_purchases'
        fact_table.to_sql(fact_table_name, con=engine, index=False, if_exists='replace')
        logger.info(f"Loaded fact table: {fact_table_name}")

        logger.info("All tables loaded successfully.")

    except Exception as e:
        logger.error("An error occurred during data loading.", exc_info=True)
        raise
