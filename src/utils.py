from typing import List

from src.constants import polygon_hierarchy


def filter_dict_by_keys_contain(in_dict: dict, filter_keys: list) -> dict:
    new_dict = dict()
    for (key, value) in in_dict.items():
        # check if key contains any of the filter_key values
        if any(filter_key in key for filter_key in filter_keys):
            new_dict[key] = value

    return new_dict


def handle_exception_product_ids(datacube_source, source_polygons_short):
    exceptions = {
        'sar_change_c_m2_automotive_car_factory': 'LVM',
        'te_car_production_sar_change_c_m2_automotive_car_factory': 'LVM',
        'te_car_registrations_sar_change_c_m2_automotive_car_factory': 'LVM',
        'sar_change_c_m2_chemical_fertilizer_inorganic': 'MAN_CHE_INO',
        'sar_change_c_m2_chemical_fertilizer_organic': 'MAN_CHE_ORG',
        'sar_c_chemical_fertilizer_inorganic_nitrogen': 'MAN_CHE_INO_NIT',
        'sar_c_chemical_fertilizer_inorganic_potash': 'MAN_CHE_INO_POT',
    }

    if datacube_source in exceptions:
        return exceptions[datacube_source]
    else:
        return source_polygons_short


def handle_exception_sources(datacube_source):
    exceptions = {
        'sar_change_c_m2_distribution_center_inland_containers': 'sar_change_c_m2_distribution_center_containers_inland_containers',
        'sar_change_c_m2_distribution_ctr_inland_containers': 'sar_change_c_m2_distribution_center_containers_inland_containers',
        'sar_change_c_m2_distribution_ctr_port_containers': 'sar_change_c_m2_distribution_center_containers_port_containers',
        'te_exports_m_sar_change_c_m2_distribution_ctr_inland_containers': 'te_exports_m_sar_change_c_m2_distribution_center_containers_inland_containers',
        'te_exports_m_sar_change_c_m2_distribution_ctr_port_containers': 'te_exports_m_sar_change_c_m2_distribution_center_containers_port_containers',
        'te_imports_m_sar_change_c_m2_distribution_ctr_port_containers': 'te_imports_m_sar_change_c_m2_distribution_center_containers_port_containers',
        'te_factory_orders_sar_change_c_m2_distribution_ctr_inland_containers': 'te_factory_orders_sar_change_c_m2_distribution_center_containers_inland_containers',
    }

    if datacube_source in exceptions:
        return exceptions[datacube_source]
    else:
        return datacube_source


def get_polygon_type_from_hierarchy(datacube_source: str, index_polygon_structure: dict) -> (str, dict):
    # TODO support multiple industries in single index
    if index_polygon_structure[0] and index_polygon_structure[1] and index_polygon_structure[2] and index_polygon_structure[3]:
        # TODO support multiple sub_type2s in single index
        relevant_polygon_hierarchies = [
            polygon_hierarchy[index_polygon_structure[0]][index_polygon_structure[1]][
                index_polygon_structure[2]][index_polygon_structure[3]],
            polygon_hierarchy[index_polygon_structure[0]][index_polygon_structure[1]][
                index_polygon_structure[2]]]
    if index_polygon_structure[0] and index_polygon_structure[1] and index_polygon_structure[2]:
        industry = index_polygon_structure[0][0]
        index_types = index_polygon_structure[1]
        index_sub_types = index_polygon_structure[2]

        relevant_polygon_hierarchies = {
            2: [polygon_hierarchy[industry][type] for type in index_polygon_structure[1]],
            3: [polygon_hierarchy[industry][type][sub_type] for sub_type in index_sub_types for type in index_types]
        }
    elif index_polygon_structure[0] and index_polygon_structure[1]:
        relevant_polygon_hierarchies = {
            1: [polygon_hierarchy[industry] for industry in index_polygon_structure[0]],
            2: [polygon_hierarchy[industry][type] for type in index_polygon_structure[1] for industry in index_polygon_structure[0]]
        }
    else:
        for industry in polygon_hierarchy:
            for polygon_type in polygon_hierarchy[industry]:
                if polygon_type in datacube_source:
                    datacube_source = datacube_source[len(polygon_type) + 1:]
                    index_polygon_structure[0].append(industry)
                    index_polygon_structure[1].append(polygon_type)
                    return datacube_source, index_polygon_structure
        return

    for level, relevant_hierarchies_level in relevant_polygon_hierarchies.items():
        for relevant_hierarchy in relevant_hierarchies_level:
            for polygon_type in relevant_hierarchy:
                if datacube_source.startswith(polygon_type):
                    datacube_source = datacube_source[len(polygon_type) + 1:]
                    index_polygon_structure[level].append(polygon_type)
                    return datacube_source, index_polygon_structure
    raise Exception(f'Unsuccessful parsing of : {datacube_source}')


def datacube_to_product_id_agr(source: str, aoi_label: str, algorithm: str) -> List[str]:
    """
    Generate possible Product IDs for a Datacube index. Works only for aggregated daily products.

    Assumption: Aggregated product name is in `source` following "sar_change_c_m2_" or "sar_c_".

    :param source:
    :param aoi_label:
    :param algorithm:
    :return: List of possible Product ID the index might belong to.
    """
    product_ids = []

    # Polygon Hierarchy
    if 'sar_change_c_m2_' in source:
        source_polygons = source.split("sar_change_c_m2_")[1]
    elif 'sar_c_' in source:
        source_polygons = source.split("sar_c_")[1]
    else:
        source_polygons = ""

    # no need to look through the product hierarchy
    source_polygons_short = source_polygons[:3].upper()

    # Product Type
    product_types = ['SAI']
    if 'black_swan' in algorithm:
        product_types = ['ASI']
    elif 'imagery_coverage_rolling' in algorithm:
        product_types.append('ASI')

    for product_type in product_types:
        product_ids.append(f'SK_AGR_{source_polygons_short}_{product_type}_{aoi_label.upper()}_D')

    return product_ids


def datacube_to_product_id(source: str, aoi_label: str, algorithm: str) -> List[str]:
    """
    Generate possible Product IDs for a Datacube index. Works only for SAI,ASI and aggregated daily products.

    :param source:
    :param aoi_label:
    :param algorithm:
    :return: List of possible Product ID the index might belong to (eg. icr index belongs to both SAI and ASI products).
    """
    if 'weighted_index' in algorithm:
        try:
            return datacube_to_product_id_agr(source, aoi_label, algorithm)
        except:
            print(f'Unsuccessful parsing of index: source={source} aoi={aoi_label} algorithm={algorithm}')
            return []

    product_ids = []
    source = handle_exception_sources(source)

    # Polygon Hierarchy
    if 'sar_change_c_m2_' in source:
        source_polygons = source.split("sar_change_c_m2_")[1]
    elif 'sar_c_' in source:
        source_polygons = source.split("sar_c_")[1]
    else:
        source_polygons = ""

    # Get polygon type
    index_polygon_structure = {
        0: [],  # industry
        1: [],  # type
        2: [],  # sub_type
        3: [],  # sub_type2
    }

    try:
        while source_polygons and len(source_polygons):
            source_polygons, index_polygon_structure = get_polygon_type_from_hierarchy(source_polygons,
                                                                                       index_polygon_structure)
    except:
        print(f'Unsuccessful parsing of index: source={source} aoi={aoi_label} algorithm={algorithm}')
        return []

    index_polygon_structure = {k: "-".join([item[:3] for item in v]).upper() for k, v in index_polygon_structure.items()}
    source_polygons_short = "_".join([part for part in index_polygon_structure.values() if part])

    source_polygons_short = handle_exception_product_ids(source, source_polygons_short)

    # Product Type
    product_types = ['SAI']
    if 'black_swan' in algorithm:
        product_types = ['ASI']
    elif 'imagery_coverage_rolling' in algorithm:
        product_types.append('ASI')

    for product_type in product_types:
        product_ids.append(f'SK_{source_polygons_short}_{product_type}_{aoi_label.upper()}_D')

    # print(product_ids)
    return product_ids


# Testing purpose
if __name__ == '__main__':
    datacube_to_product_id('sar_change_c_m2_construction_cement', 'gb', 'black_swan')
    datacube_to_product_id('sar_change_c_m2_wood_sawmill_woodchip', 'de', 'black_swan')
    datacube_to_product_id('sar_change_c_m2_distribution_center_inland_containers', 'de', 'black_swan')
