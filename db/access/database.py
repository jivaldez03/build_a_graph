from db.access.config import settings_any

def driver_open_session():
    port = input (f"port to connect Neo4j ({settings_any.db.NEO4J_PORT}): ")
    if not port:
        port = settings_any.db.NEO4J_PORT
    target_db = settings_any.open_driver(port)
    return target_db

def driver_close():
    settings_any.connection.close()
