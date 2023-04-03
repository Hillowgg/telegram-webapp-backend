from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(openapi_prefix='/api')




@app.on_event("startup")
async def startup_event():
    register_tortoise(
        app,
        db_url='sqlite://db.sqlite3',
        modules={'models': ['backend.src.models']},
        generate_schemas=False,
        add_exception_handlers=True
    )

# 'query_id=AAEa-cALAAAAABr5wAsl8McX&user={'id':197196058,'first_name':'Hillow','last_name':'','username':'Hillow','language_code':'en'}&auth_date=1676290535&hash=05a2fad9bae858663aacdba807dc986588b0ccbafb3f221baa48d493ecf0ed2e'
