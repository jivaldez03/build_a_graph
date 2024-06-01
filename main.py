from app.general_functions import pandas_fn as pd_fns
from db.access.database import driver_open_session, driver_close
import app.loading_fn as loadf 

# MAIN SECTION
driver_open_session()

loadf.initializing_database()

pdxls = pd_fns._read_filexlsx('files/bag_file001.xlsx') #,sheetname='Sheet1') 
print("sheets: ", pdxls.keys())
for gia, sheet in enumerate(list(pdxls.keys())[0:]):
    print(f"\nsheet: {sheet}")
    if not sheet in ['Sheet1']:
        continue
    df = pdxls[sheet]
    cols = list(df.columns)
    loadf.nodes(df)

driver_close()

