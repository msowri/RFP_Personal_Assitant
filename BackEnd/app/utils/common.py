
def success_response(data=None, message="Success"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def error_response(message="Error", status="error"):
    return {
        "status": status,
        "message": message
    }