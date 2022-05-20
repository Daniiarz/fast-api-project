from databases import Database
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://test:test@127.0.0.1:5445/test"

engine = create_engine(DATABASE_URL, future=True, echo=True)
database = Database(DATABASE_URL)

#  Using context manager to open and close connection
# with async_engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all())


# #  Insertion of many rows into the table specifying list of values
# with async_engine.connect() as conn:
#     conn.execute(text("create table if not exists test_table (x int, y int)"))
#     conn.execute(
#         text("insert into test_table (x, y) values (:x, :y)"),
#         [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
#     )
#     conn.commit()

# # Returned result object is a named tuple values of which we can access by index, attribute
# with async_engine.connect() as conn:
#     result = conn.execute(text("select * from test_table"))
#     for row in result:
#         print(f"x: {row.x}, y: {row.y}")


# # Binding params allows passing a parameter to sql statement
# stmt = text("SELECT x, y FROM test_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
# with async_engine.connect() as conn:
#     result = conn.execute(stmt)
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")

# Session object is the same as connection object but, used mostly for ORM
# stmt = text("SELECT x, y FROM test_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
# with Session(async_engine) as session:
#     result = session.execute(stmt)
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")
