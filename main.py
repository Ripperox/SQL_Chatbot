from py_modules import *

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
generate_query = create_sql_query_chain(llm, db)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key="hello")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    request.session['key'] = 'hello'
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/generate-query/", response_class=HTMLResponse)
async def generate_query_endpoint(request: Request, question: str = Form(...)):
    try:
        query = generate_query.invoke({"question": question})
        execute_query = QuerySQLDataBaseTool(db=db)
        result_str = execute_query.invoke(query)
        result = ast.literal_eval(result_str)

        dataframe = create_dataframe(result, query)
        
        image_data, summary = visualizer(dataframe, question)

        if isinstance(image_data, str):
            return templates.TemplateResponse("error.html", {"request": request, "message": image_data})

        dataframe_html = dataframe.to_html(index=False)

        request.session['query'] = query
        request.session['graph_code'] = image_data.code
        request.session['dataframe_html'] = dataframe_html
        request.session['summary'] = summary
        request.session['question'] = question

        return templates.TemplateResponse("result.html", {
            "request": request,
            "query": query,
            "dataframe_html": dataframe_html,
            "graph": image_data.raster
        })

    except Exception as e:
        logging.error(f"Error generating or executing query: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "message": str(e)})

@app.post("/edit-graph/", response_class=HTMLResponse)
async def edit_graph_endpoint(request: Request, specifications: str = Form(...)):
    try:
        query = request.session.get('query', '')
        graph_code = request.session.get('graph_code', '')
        summary = request.session.get('summary', '')
        dataframe_html = request.session.get('dataframe_html', '')
        edited_image, edited_summary = edit(graph_code, specifications, summary)

        if isinstance(edited_image, str):
            return templates.TemplateResponse("error.html", {"request": request, "message": edited_image})
        
        request.session['query'] = query
        request.session['graph_code'] = edited_image.code  
        request.session['summary'] = edited_summary 
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "query": query,
            "dataframe_html": dataframe_html,
            "graph": edited_image.raster
        })

    except Exception as e:
        logging.error(f"Error in editing graph: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "message": str(e)})

@app.post("/submit-feedback/", response_class=JSONResponse)
async def submit_feedback(request: Request, feedback: str = Form(...)):
    try:
        question = request.session.get('question', '')
        sql_query = request.session.get('query', '')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO feedback (question, sql_query, feedback)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (question, sql_query, feedback))
        conn.commit()
        
        cursor.close()
        conn.close()

        return JSONResponse(content={"message": "Feedback submitted successfully"})

    except Exception as e:
        logging.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Error submitting feedback")

