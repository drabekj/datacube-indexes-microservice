# polygon_types_to_industry = {
#     'airports': 'transport',
#     'automotive': 'automotive',
#     'chemical': 'manufacturing',
#     'construction': 'manufacturing',
#     'defence_aerospace': 'manufacturing',
#     'distribution_center': 'transport',
#     'electronics': 'manufacturing',
#     'field': 'mining',
#     'food': 'manufacturing',
#     'heavy_industry': 'manufacturing',
#     'heavy': 'manufacturing',
#     'metal': 'manufacturing',
#     'mine': 'mining',
#     'ports': 'transport',
#     'power_plant': 'energy',
#     'processing': 'mining',
#     'textile': 'manufacturing',
#     'waste': 'utilities',
#     'water': 'utilities',
#     'wood': 'manufacturing',
# }

polygon_hierarchy = {
    'energy': {
        'power_plant': {
            'hydro': {},
            'coal': {},
            'oil_gas': {},
            'biomass': {},
            'geothermal': {},
            'nuclear': {},
            'waste': {},
        },
    },
    'manufacturing': {
        'construction': {
            'building_supplies': {},
            'ship_construction': {},
            'cement': {
                'refinery': {},
                'storage': {},
            },
            'aviation': {},
        },
        'metal': {
            'copper': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'steel': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'lead': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'aluminium': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'iron': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'zinc': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'nickel': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'tin': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'unknown': {
                'storage': {},
                'refinery': {},
                'scrap': {},
            },
            'rare': {},
        },
        'automotive': {
            'car_factory': {},
            'bus_factory': {},
            'truck_factory': {},
            'tractor_factory': {},
            'engines': {},
            'tires': {},
        },
        'food': {
            'sugar': {},
            'beverage': {},
            'produce': {},
        },
        'chemical': {
            'fertilizer_organic': {},
            'fertilizer_inorganic': {
                'potash': {},
                'nitrogen': {},
                'phosphate': {},
            },
            'plastic': {},
            'liquid_fuels': {},
            'glass': {},
            'rubber': {},
        },
        'defence_aerospace': {},
        'wood': {
            'sawmill': {},
            'woodchip': {},
            'paper_processing': {},
        },
        'textile': {
            'paper_processing': {},
        },
        'electronics': {
            'appliances': {},
            'phones': {},
        },
        'heavy_industry': {
            'locomotive': {},
            'large_machines': {},
        },
    },
    'mining': {
        'mine': {
            'ore': {
                'platinum': {
                    'underground': {},
                    'open_pit': {},
                },
                'diamond': {
                    'underground': {},
                    'open_pit': {},
                },
                'gold': {
                    'underground': {},
                    'open_pit': {},
                },
                'silver': {
                    'underground': {},
                    'open_pit': {},
                },
                'zinc': {
                    'underground': {},
                    'open_pit': {},
                },
                'nickel': {
                    'underground': {},
                    'open_pit': {},
                },
                'copper': {
                    'underground': {},
                    'open_pit': {},
                },
                'bauxite': {
                    'underground': {},
                    'open_pit': {},
                },
                'lithium': {
                    'underground': {},
                    'open_pit': {},
                },
                'iron': {
                    'underground': {},
                    'open_pit': {},
                },
                'unknown': {
                    'underground': {},
                    'open_pit': {},
                },
            },
            'non_ore': {
                'limestone': {},
                'sand': {},
            },
            'coal': {},
        },
        'field': {
            'oil_gas': {},
        },
        'processing': {
            'coal': {},
            'platinum': {},
            'diamond': {},
        },
    },
    'transport': {
        'distribution_center': {
            'containers': {
                'inland_containers': {},
                'port_containers': {},
                'train_station': {},
            },
            'pipes': {},
            'wood': {},
            'coal': {},
            'cars': {},
            'minerals': {},
            'waste': {},
            'liquid_fuels': {},
        },
        'airports': {
            'passenger': {},
            'cargo': {},
            'military': {},
            'private': {},
        },
        'ports': {
            'liquid_fuels': {},
            'wood': {},
            'industrial': {},
            'marina': {},
            'naval_base': {},
        },
    },
    'utilities': {
        'waste': {
            'landfill': {},
            'transfer_station': {},
            'reprocessing': {},
        },
        'water': {
            'waste': {},
            'desalination': {},
        },
    },
}