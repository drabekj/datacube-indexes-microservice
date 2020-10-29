from typing import List

from src.constants import polygon_types_to_industry


def filter_dict_by_keys_contain(in_dict: dict, filter_keys: list) -> dict:
    new_dict = dict()
    for (key, value) in in_dict.items():
        # check if key contains any of the filter_key values
        if any(filter_key in key for filter_key in filter_keys):
            new_dict[key] = value

    return new_dict


def datacube_to_product_id(source: str, aoi_label: str, algorithm: str) -> List[str]:
    """
    Generate possible Product IDs for a Datacube index. Works only for SAI and SAI daily products.

    :param source:
    :param aoi_label:
    :param algorithm:
    :return:
    """
    product_ids = []

    # Polygon Hierarchy
    source_polygons_parts = []
    if 'sar_change_c_m2_' in source:
        source_polygons_parts = source.split("sar_change_c_m2_")[1].split("_")
    elif 'sar_c_' in source:
        source_polygons_parts = source.split("sar_c_")[1].split("_")
    industry_short = polygon_types_to_industry[source_polygons_parts[0]][:3].upper()
    source_polygons_short = [part[:3].upper() for part in source_polygons_parts]
    source_polygons_short = industry_short + "_" + '_'.join(source_polygons_short)

    # Product Type
    product_types = ['SAI']
    if 'black_swan' in algorithm:
        product_types = ['ASI']
    elif 'imagery_coverage_rolling' in algorithm:
        product_types.append('ASI')

    for product_type in product_types:
        product_ids.append(f'SK_{source_polygons_short}_{product_type}_{aoi_label.upper()}_D')

    return product_ids
