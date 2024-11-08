from brick_utils import load_graph
from ahu_info import identify_ahu_equipment, print_ahu_info
from zone_info import identify_zone_equipment, print_zone_info
from meters_info import query_building_area, query_meters, print_meter_info
from central_plant_info import identify_hvac_system_equipment, print_central_plant_info

def main():
    file_path = "./bldg11.ttl"  # Path to your TTL file
    graph = load_graph(file_path)

    # Process AHU information
    ahu_info = identify_ahu_equipment(graph)
    print_ahu_info(ahu_info)

    # Process zone information
    zone_info = identify_zone_equipment(graph)
    print_zone_info(zone_info)

    # Process meter information
    building_area = query_building_area(graph)
    meter_info = query_meters(graph)
    print_meter_info(meter_info, building_area)

    # Process central plant information
    hvac_info = identify_hvac_system_equipment(graph)
    print_central_plant_info(hvac_info)

if __name__ == "__main__":
    main()
