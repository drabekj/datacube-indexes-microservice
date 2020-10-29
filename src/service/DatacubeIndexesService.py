from src.service.fetch_datacube import DatacubeService
from src.utils import filter_dict_by_keys_contain, datacube_to_product_id

SAI_ASI_ALGORITHMS = ['rolling_activity_index_value', 'imagery_coverage_rolling',
                      'rolling_black_swan_negative_anomaly', 'rolling_black_swan_normal_range',
                      'rolling_black_swan_positive_anomaly']


class DatacubeIndexesService:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token

    def get_indexes_by_product_id(self, filter_algorithms=SAI_ASI_ALGORITHMS) -> dict:
        """
        Get indexes from Datacube, grouped by Product ID. Only filter_algorithms will be presented.
        :return: dict where key is Product ID and value is a list of dists of the index attributes.
        """
        full_datacube_catalog = DatacubeService(self.bearer_token).get_catalogue_data()
        index_catalog = filter_dict_by_keys_contain(full_datacube_catalog, filter_algorithms)

        indexes_by_product = {}
        for algorithm in index_catalog:
            for index_dict in index_catalog[algorithm]:
                product_ids = datacube_to_product_id(index_dict['source'], index_dict['aoi_label'], algorithm)

                for product_id in product_ids:
                    indexes_by_product.setdefault(product_id, []).append({
                        'source': index_dict['source'],
                        'aoi_label': index_dict['aoi_label'],
                        'algorithm': algorithm,
                        'version': index_dict['version']
                    })

        return indexes_by_product
