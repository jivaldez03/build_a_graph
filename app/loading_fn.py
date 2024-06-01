from db import common_dbfunc as dbexec
#from app.db.database import targetdb
#from db.crud.NIST_file import control, control_enhancement
import db.crud.crud_loadf as loadf
from app.general_functions.pandas_fn import _df_NaNbyAny


def initializing_database():
    query = """
            match (n)
            detach delete (n)
            """
    print(f"Initializing database ...")
    dbexec.execute_write_query(query)

def nodes(df):
    def clean_node_value(node_value):
        node, id = node_value.split('::')
        if isinstance(id, str):
            id = id.title()
        return node.capitalize(), id
    
    def nodes_and_relationship(node_source, node_target, relationship, attribute_relationship, attribute_value):
        query = loadf.NODES

        source_label, source_id = clean_node_value(node_source)
        target_label, target_id = clean_node_value(node_target)
        
        query = query.format(SOURCE_LABEL=source_label
                            , TARGET_LABEL=target_label
                            , RELATIONSHIP=relationship
                            , ID_SOURCE='{ID:$source_code}'
                            , ID_TARGET='{ID:$target_code}'
                            )
        print('query:', query)
        dbexec.execute_write_query(query
                            , source_code = source_id
                            , target_code = target_id
                            )
        if attribute_relationship:
            attribute_relationship = attribute_relationship.strip().lower()

            query = loadf.ATTRIBUTE_RELATIONSHIP
            
            query = query.format(SOURCE_LABEL=source_label
                                , TARGET_LABEL=target_label
                                , RELATIONSHIP=relationship
                                , ID_SOURCE='{ID:$source_code}'
                                , ID_TARGET='{ID:$target_code}'
                                , ATTRIBUTE=attribute_relationship
                                , ATTRIBUTE_VALUE = '$attribute_value'
                                )
            print('query:', query)
            dbexec.execute_write_query(query
                                , source_code = source_id
                                , target_code = target_id
                                , attribute_value = attribute_value
                                )
            
        
        return
    
    def attribute_for_a_node(node_source, attribute, value):
        query = loadf.ATTRIBUTE

        source_label, source_id = clean_node_value(node_source)
        attribute = attribute.strip().lower()
        attribute_value = value
        
        query = query.format(SOURCE_LABEL=source_label
                            , ID_SOURCE='{ID:$source_code}'
                            , ATTRIBUTE=attribute
                            , ATTRIBUTE_VALUE='$attribute_value'
                            )
        print('query:', query)
        dbexec.execute_write_query(query
                            , source_code = source_id
                            , attribute_value = attribute_value
                            )



    print("Adding Nodes")
    df = _df_NaNbyAny(df, changeto=None)
    for index_df, row in df.iterrows():
        #print(f"index: {index_df}")
        index = index_df
        node_source = row['Item']
        node_target = row['Object']
        relationship = row['Relationship'].strip().upper().replace(' ','_')
        Relationship_Property = row['Relationship_Property']
        Relationship_Value = row['Relationship_Value']

        if isinstance(node_target, str):
            # is the row a relationship betweens nodes?
            if node_source.__contains__('::'):
                if node_target.__contains__('::'): # it is a relationships between nodes                                        
                    #print('node + node', index, node_source, node_target, Relationship_Property, Relationship_Value)                    
                    nodes_and_relationship(node_source, node_target, relationship, Relationship_Property, Relationship_Value)                        
                else:   # is an attribute for node_source
                    #print('node + att', index, node_source, node_target)
                    attribute_for_a_node(node_source, attribute=relationship, value=node_target)
        else:            
            #print('node + num att', index, node_source, node_target)
            attribute_for_a_node(node_source, attribute=relationship, value=node_target)  
            
    return
