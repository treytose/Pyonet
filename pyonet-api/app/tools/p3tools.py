from app import db
import traceback, os

def excHandler(func):
    def inner(self, *args, **kwargs):
        try:
            resp = func(self, *args, **kwargs)
            return resp
        except KeyError as ke:
            self.log_error('KeyError: ' + str(traceback.format_exc()))
            return {'error': 8, 'message': f'KeyError in API - Make sure you are passing the proper JSON object with correctly named keys! Error: {str(ke)}', 'data': {}}
        except Exception as e:
            self.log_error('API exception occured: ' + str(traceback.format_exc()))
            return {'error': 6, 'message': 'An unknown error occured', 'data': {}}
    return inner


async def get_schema(model):    
    schema = model.schema()
    for v in schema['properties'].values():
        allowed_values = v.get("form_options", {}).get("allowed_values")
        if allowed_values and isinstance(allowed_values, str) and str.startswith(allowed_values.upper(), "SELECT"):                                
            v["form_options"]["allowed_values"] = await db.fetchall(allowed_values)                            
    
    return schema