def success_response(data=None, message="Success"):
    return {"message": message, "data": data}, 200

def error_response(message="Error", status=400):
    return {"message": message}, status
