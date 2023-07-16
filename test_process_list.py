import pytest
import process_list

def main():
    print("testing test_process_list.py")
    pass

def test_latitude_next():
    """is_latitiude_next should only trigger when a number starts with 15 """
    assert process_list.is_latitude_next("15.34") == True
    assert process_list.is_latitude_next("15,34") == True
    assert process_list.is_latitude_next("15345") == False
    assert process_list.is_latitude_next("11.245") == False
    assert process_list.is_latitude_next("abcde") == False

def test_longitude_next():
    """is_longitude_next should only return true when starts with 120"""
    assert process_list.is_longitude_next("120.4") == True
    assert process_list.is_longitude_next("120,4") == True
    assert process_list.is_longitude_next("12023") == False
    assert process_list.is_longitude_next("11.24") == False
    assert process_list.is_longitude_next("abcde") == False
    assert process_list.is_longitude_next("11815") == False
    assert process_list.is_longitude_next("139\n") == False
    assert process_list.is_longitude_next("139\r") == False
    assert process_list.is_longitude_next("167 |") == False

def test_first_two_data_rows():
    """this function takes the first two dataliens of the original text
    file, because these lines seem to illustrate an odd interaction seen
    throughout the text file whereby \n seems to be read as a number"""
    
    file_name = r"./test_data/first_two_data_rows.txt"
    with open(file_name, "r", encoding="utf-8") as file:
        reader = file.readlines()
        for row in reader:
            pass
    pass

    

if __name__ == "__main__":
    main()