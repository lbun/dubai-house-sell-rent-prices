import duckdb
import os

azure_con_string = os.getenv("storage_account_datasciencetest2024_connection_string", None)

class DuckClient:
    def __init__(self, azure_con_string=None, db_name=None):
         self.azure_con_string = azure_con_string
         self.db_name = db_name

    def get_client(self):
        if self.db_name:
            con = duckdb.connect(self.db_name, config={"allow_unsigned_extensions": "true"})
        else:
            con = duckdb.connect(config={"allow_unsigned_extensions": "true"})
        # Installing libraries
        con.execute("INSTALL SPATIAL;")
        con.execute("LOAD SPATIAL")
        con.install_extension("httpfs")
        con.load_extension("httpfs")
        con.install_extension("azure")
        con.load_extension("azure")

        # con.execute("SET allow_community_extensions = true;")

        # Installing h3
        con.execute("FORCE INSTALL h3 FROM community;")
        con.execute("LOAD H3")

        if self.azure_con_string:
            con.execute(f"""CREATE SECRET secret1 (
                            TYPE AZURE,
                            CONNECTION_STRING '{self.azure_con_string}'
                        );""")
        return con