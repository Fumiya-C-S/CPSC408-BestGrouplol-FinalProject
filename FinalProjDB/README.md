## Instructions
    1. First we need to download Node JS from https://nodejs.org/en/download/current 
    If you are using VSCODE open up a terminal. 
    Do node -v. 
    You should get v25.2.1. 
    Also do npm -v.
    We should get 11.6.2. 

    2. Do the ls command. We should see a folder FinalProjDB. 
    3. cd FinalProjDB. 
    4. cd db-project
    5. npm install - to install dependencies. 
    We need two terminals to run. So for vscode go up top where it says terminal and click split terminal. 
    We need one terminal in the directory db-project and another one in the directory FinalProjDB. 
    The one in db-project will run our react code using vite. 
    The one in FinalProjDB will run our back end using uvicorn. 
    6. Step 6 is to have the database in the local computer.
    7. Verify the correct information in the file dbInterface.py get_db_connection() funcition matches the database name. 
    8. On ther terminal for FinalProjDB do the command: uvicorn dbInterface:app --reload
    Which will create an instance of our fastapi backend in our local host. 
    You will get some output like this.  Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit).
    All of our fethces are done with this url so make sure it matches!
    9. Next on the terminal that is in db-project do the command: npm run dev
    10. You will have been given a url from the terimal. Something like: Local:   http://localhost:5173/
    11. Paste the url to your browser. 
    12. Interact with the application. 
## Resource Used
    Basic React: 
    https://www.youtube.com/watch?v=CgkZ7MvWUAA 
    https://www.youtube.com/watch?v=SqcY0GlETPk  
    FastApi:
    https://www.youtube.com/watch?v=tLKKmouUams  
    https://www.youtube.com/watch?v=aSdVU9-SxH4 
    https://www.youtube.com/watch?v=zzOwU41UjTM 
    https://www.youtube.com/watch?v=GONyd0CUrPc  
    https://www.youtube.com/watch?v=pRYzMF04fLw&t=784s 
    React Fetch: 
    https://www.youtube.com/watch?v=00lxm_doFYw 
    https://www.youtube.com/watch?v=qdCHEUaFhBk 
    https://www.youtube.com/watch?v=MBlZ8Wzkbi4 
    React Router:
    https://www.youtube.com/watch?v=oTIJunBa6MA 
    https://www.youtube.com/watch?v=NVuxUktUvxc 
    Offical Docs for react router: 
    https://reactrouter.com/6.30.2/start/tutorial 
    Navigation bar inspiration: 
    https://www.youtube.com/watch?v=5mO-T2o9zuk 
    https://www.youtube.com/watch?v=f3uCSh6LIY0 
    Other than the Navigaiton bar which was more specific. The list of videos and docs allowed us to generally grasp what to do given our goals for react and setting up or backend with sql. 
## Minimum requirements met
    We were able to create a multitide of queries in our app.py but only able to incoroproate a hand full in our project. Nevertheless we did do a good effort on the project. 
## Youtube Demo Link
    https://www.youtube.com/watch?v=PcsuaUSYi_Q 
## LLM USAGE
    1. For using fastapi i was familiar of how to use get requests from youtube videos from the resource used. However I had an issue with post requests that CHATGPT helped resolve. 
    This was a stream of back and forth question and answers. 
    Me: 
    For a post method i get {"detail":"Method Not Allowed"}
    GPT:
    {"detail":"Method Not Allowed"} means:
    👉 You are calling a POST on a route that is NOT defined as POST.
    (or you are calling the wrong URL, or the server wasn't reloaded.)
    This error comes from FastAPI + Uvicorn, not from your database.
    Let’s walk through every possible cause and how to fix it.

    ✅ 1. You defined GET but you're calling POST
    Example mistake:
    @app.get("/create_view")
    def create_view():
        ...

    But your client/browser/API tool sends:
    POST /create_view

    FastAPI responds:
    405 Method Not Allowed

    Fix: Change the decorator:
    @app.post("/create_view")
    def create_view():
        ...


    ✅ 2. You updated the code, but Uvicorn didn’t reload
    If you ran:
    uvicorn dbinterface:app

    (without --reload), then FastAPI won't reload after code changes.
    Fix:
    uvicorn dbinterface:app --reload


    ✅ 3. You’re calling the wrong URL
    Check:
    The path in your FastAPI code


    The path you're sending the request to


    Example:
    If code says:
    @app.post("/make_view")

    But you're calling:
    POST /create_view

    → 405.

    ✅ 4. You’re sending POST from the browser URL bar
    Typing:
    http://localhost:8000/create_view

    Always sends GET, never POST.
    Use:
    Swagger UI → http://127.0.0.1:8000/docs
    Postman
    curl
    Python client

    Example curl:
    curl -X POST http://127.0.0.1:8000/create_view


    ✅ 5. There is another route shadowing it
    Example:
    @app.get("/{something}")
    def catch_all(something: str):
        ...

    This could block:
    POST /create_view
    Fix: move your POST route above wildcard routes.

    🔥 Quick test: does FastAPI see your POST?
    Open:
    http://127.0.0.1:8000/openapi.json

    Search for your route:
    If it's NOT there, FastAPI never loaded it → code not running or wrong file.
    If it's there under GET but not POST → decorator issue.

    🚀 If you want, paste your route code and I’ll tell you exactly what's wrong.
    Even just:
    your route decorator
    your function
    your uvicorn command
    your file name
    I can pinpoint the cause in seconds.
    Me: 
    Im using the docs for the execute the post request. I was using the url lol. But now i got this. Curl curl -X 'POST' \ 'http://127.0.0.1:8000/create_view/?customer_id=1' \ -H 'accept: application/json' \ -d '' Request URL http://127.0.0.1:8000/create_view/?customer_id=1 Server response Code	Details 500 Undocumented Error: Internal Server Error Response body Download Internal Server Error Response headers content-length: 21 content-type: text/plain; charset=utf-8 date: Fri,12 Dec 2025 19:29:23 GMT server: uvicorn
    A 500 Internal Server Error means your POST route was called correctly, but your Python code threw an exception inside the route.

    This is good — now we know the routing is correct.
    Now we fix the internal error.

    ✅ Step 1 — View the REAL error (the traceback)
    Open the terminal running Uvicorn.
    You should see something like:
    ERROR: Exception in ASGI application
    Traceback (most recent call last):
    ...

    Paste that traceback here — that will show the exact cause.

    🔥 Common causes (likely one of these)
    Since you're creating a SQL view, here are the most likely reasons:

    ❌ 1. You're using Query parameters but the function signature expects something else
    Example:
    Calling:
    /create_view/?customer_id=1

    But function is:
    @app.post("/create_view")
    def create_view(customer_id: int):
        ...

    This is correct — FastAPI will match customer_id.
    But if your argument names don't match:
    def create_view(id: int):

    Then customer_id won’t be passed → FastAPI responds:
    422 Unprocessable Entity

    Not your case — you got 500.
    So we move on.

    ❌ 2. Database error when running CREATE VIEW
    Most common:
    View already exists

    Bad SQL syntax
    Wrong table name
    Connection closed
    Cursor reused after commit
    SQLite requires special handling for views
    You didn’t commit properly
    You’re using .execute() incorrectly with async handlers

    ❌ 3. You forgot to return something or returned a non-serializable type
    Example:
    return cursor.execute(...)

    This returns None or a DB cursor → cannot be converted to JSON → 500

    ❌ 4. You used async def with a synchronous DB driver
    Example:
    @app.post("/create_view")
    async def create_view():
        cursor.execute(...)   # sync I/O inside async function

    SQLite in particular will throw:
    ProgrammingError: SQLite objects created in a thread can only be used in that same thread


    🚀 To give you the exact fix, paste this:
    1. Your route code:
    @app.post("/create_view")
    def create_view(...):
        ...

    2. Your database code in that function
    3. The traceback from the uvicorn console
    With those 3 pieces, I can pinpoint the exact cause and give you the corrected code.

    Me: 
    @app.post('/create_view/') def create_view(customer_id: str, db_ops = Depends(get_db_connection)): cursor = db_ops.cursor(dictionary=True) create_view = f''' CREATE VIEW users_order AS SELECT o.OrderID, o.OrderDate, o.Status FROM Orders AS o WHERE CustomerID = {customer_id}; ''' cursor.execute(create_view, list(customer_id)) cursor.commit() cursor.close() return {"Result": "View was created"}

    GPT:
    You're very close, but there are 3 MAJOR errors in your code that will cause a 500 Internal Server Error every time.
    I'll show each issue, then give you the correct version.

    ❌ ERROR 1 — Wrong usage of string formatting + SQL parameters
    You wrote:
    create_view = f'''
    CREATE VIEW users_order AS
    SELECT o.OrderID, o.OrderDate, o.Status
    FROM Orders AS o
    WHERE CustomerID = {customer_id};
    '''
    cursor.execute(create_view, list(customer_id))

    This is wrong because:
    ❌ You already put the value inside the f-string
    → Using parameters (the second argument of .execute()) doesn’t work anymore.
    ❌ list(customer_id) is incorrect
    If customer_id="1", list("1") becomes ['1'].
    If customer_id="123", list("123") becomes ['1','2','3'].
    This will break the SQL execution.

    ❌ ERROR 2 — Trying to use parameters inside CREATE VIEW
    MySQL / MariaDB / PostgreSQL do NOT allow binding params when creating a view, e.g.:
    CREATE VIEW ... WHERE CustomerID = %s
    will not work.
    You must embed it into the SQL string.

    ❌ ERROR 3 — Using .commit() on the cursor instead of the connection
    cursor.commit()

    cursor.commit() does not exist.
    Commit must be applied to the connection, not the cursor.

    ❌ ERROR 4 — dictionary=True does not exist for many DB cursor types
    If you're using MySQL or SQLite, this may be invalid.

    ❌ ERROR 5 — SQL injection vulnerability
    This code:
    WHERE CustomerID = {customer_id}

    lets a user do:
    ?customer_id=1; DROP TABLE Orders;

    Boom — your database is gone.
    We must validate the ID.

    ✅ Corrected version (safe, working)
    @app.post('/create_view/')
    def create_view(customer_id: int, db_ops = Depends(get_db_connection)):
        cursor = db_ops.cursor()

        # SAFE validation (integer only)
        customer_id = int(customer_id)

        # Build the view creation SQL
        create_view_sql = f"""
        CREATE OR REPLACE VIEW users_order AS
        SELECT o.OrderID, o.OrderDate, o.Status
        FROM Orders AS o
        WHERE CustomerID = {customer_id};
        """

        # Execute SQL
        cursor.execute(create_view_sql)

        # Commit using the connection, NOT the cursor
        db_ops.commit()

        cursor.close()
        return {"Result": "View created successfully"}

    It influenced my code to this. 
    @app.post('/create_view/')
    def create_view(customer_id: str, db_ops = Depends(get_db_connection)):
        cursor = db_ops.cursor(dictionary=True)
        create_view = f'''
        CREATE VIEW users_order AS
        SELECT o.OrderID, o.OrderDate, o.Status
        FROM Orders AS o
        WHERE CustomerID = {customer_id};
        '''
        cursor.execute(create_view)
        db_ops.commit()
        cursor.close()
        return {"Result": "View was created"}

    It was originally this: 
    @app.post('/create_view/') 
    def create_view(customer_id: str, db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary=True) 
    create_view = f'''
    CREATE VIEW users_order AS SELECT o.OrderID, o.OrderDate, 
    o.Status FROM Orders AS o WHERE CustomerID = {customer_id}; ''' 
    cursor.execute(create_view, list(customer_id)) 
    cursor.commit() 
    cursor.close() 
    return {"Result": "View was created"}

