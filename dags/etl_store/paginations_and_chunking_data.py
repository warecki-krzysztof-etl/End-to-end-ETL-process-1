import time

def simulate_pagination(number_of_pages : int):
    for nr in range(1, number_of_pages + 1, 1):
        time.sleep(1)
        try:
            yield (f"Data from page {nr}!")
        finally:
            pass

def chunk_data(large_list : list, package_size : int):
    print(f"[SYSTEM] Chunks {len(large_list)}-element list to {package_size} packs")
    for pack in range(0, len(large_list), package_size):
        time.sleep(0.25)
        actual_pack = large_list[pack : pack + package_size]
        try:
            yield actual_pack
        finally:
            pass

if __name__ == "__main__":
    print("------TEST - ASSIGNMENT NO. 1---------")
    for api_pack in simulate_pagination(number_of_pages=3):
        print(f"Received from generator: {api_pack}")

    print("------TEST - ASSIGNMENT NO. 2---------")
    big_data_size = list(range(1,1001))
    pack_number = 1
    for chunk in chunk_data(large_list=big_data_size, package_size=100):
        print(f"Package no {pack_number} contains {len(chunk)} elements. First one is - {chunk[0]}")
        pack_number += 1
        