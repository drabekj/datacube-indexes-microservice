import os
import flask

from src import factory_build_app
from src.service.DatacubeIndexesService import DatacubeIndexesService

app = factory_build_app(os.getenv('BOILERPLATE_ENV') or 'dev')

HTTP_HOST = os.getenv('HTTP_HOST', '127.0.0.1')
HTTP_PORT = int(os.getenv('HTTP_PORT', '5001'))


@app.route('/', methods=['POST'])
def pull_economic_indexes_local():
    return pull_economic_indexes(flask.request)


def pull_economic_indexes(request):
    """
    Pull SpaceKnow economic products from the Product API.

    expected request format:
    {
        authentiactionToken: "",
        products: [productId]
    }

    :return: Dict with success status.
    """
    datacube_index_service = DatacubeIndexesService(request.json.get('authenticationToken'))
    index_catalog = datacube_index_service.get_indexes_by_product_id()

    return {
        'status': 'success',
        'results': index_catalog
    }


def handle_http_event(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    return pull_economic_indexes(request)


if __name__ == '__main__':
    app.run(host=HTTP_HOST, port=HTTP_PORT)
