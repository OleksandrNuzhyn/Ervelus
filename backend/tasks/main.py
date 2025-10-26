from flask import Flask, request, Response
import resize_handler 
import delete_handler
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/image-delete', methods=['POST'])
def image_delete_handler():
    try:
        data = request.get_json()
        if not data:
            logging.error("Request is empty")
            return Response(status=204)

        delete_handler.image_delete(data)
        return Response(status=204)
    except Exception as e:
        logging.error("Error while processing image delete", extra={'error': str(e)}, exc_info=True)
        return Response(status=204)

@app.route('/image-resize', methods=['POST'])
def image_resize_handler():
    try:
        data = request.get_json()
        if not data:
            logging.error("Request is empty")
            return Response(status=204)

        resize_handler.image_resize(data)
        return Response(status=204)
    except Exception as e:
        logging.error("Error while processing image resize", extra={'error': str(e)}, exc_info=True)
        return Response(status=204)