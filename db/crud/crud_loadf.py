NODES = """
        MERGE (S:{SOURCE_LABEL} {ID_SOURCE})
        on create set S.ctInsert = datetime()
        on match set S.ctUpdate = datetime()
        MERGE (T:{TARGET_LABEL} {ID_TARGET})
        on create set T.ctInsert = datetime()
        on match set T.ctUpdate = datetime()
        MERGE (S)-[:{RELATIONSHIP}]->(T)        
        """
ATTRIBUTE_RELATIONSHIP = """
        MATCH (S:{SOURCE_LABEL} {ID_SOURCE})
        MATCH (T:{TARGET_LABEL} {ID_TARGET})
        MATCH (S)-[R:{RELATIONSHIP}]->(T)
        SET R.{ATTRIBUTE} = {ATTRIBUTE_VALUE}
            , R.ctUpdate = datetime()
        """

ATTRIBUTE = """
        MATCH (S:{SOURCE_LABEL} {ID_SOURCE})
        SET S.ctUpdate = datetime()
            , S.{ATTRIBUTE} = {ATTRIBUTE_VALUE}
        """

create_category_prop = """set C += {{ {properties} }}
                return C
                """