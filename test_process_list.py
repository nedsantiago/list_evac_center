import pytest
import process_list

def main():
    print("testing test_process_list.py")
    test_latitude_next()
    test_longitude_next()
    test_first_two_data_rows()
    pass

def test_latitude_next():
    """is_latitiude_next should only trigger when a number starts with 15 """
    processor = process_list.evac_list_processor()
    assert processor.is_latitude_next("15.34") == True
    assert processor.is_latitude_next("15,34") == True
    assert processor.is_latitude_next("15345") == False
    assert processor.is_latitude_next("11.245") == False
    assert processor.is_latitude_next("abcde") == False

def test_longitude_next():
    """is_longitude_next should only return true when starts with 120"""

    processor = process_list.evac_list_processor()
    assert processor.is_longitude_next("120.4") == True
    assert processor.is_longitude_next("120,4") == True
    assert processor.is_longitude_next("12023") == False
    assert processor.is_longitude_next("11.24") == False
    assert processor.is_longitude_next("abcde") == False
    assert processor.is_longitude_next("11815") == False
    assert processor.is_longitude_next("139\n") == False
    assert processor.is_longitude_next("139\r") == False
    assert processor.is_longitude_next("167 |") == False

def test_first_two_data_rows():
    """this function takes the first two dataliens of the original text
    file, because these lines seem to illustrate an odd interaction seen
    throughout the text file whereby \n seems to be read as a number"""

    processor = process_list.evac_list_processor()
    
    file_name = r"./test_data/first_two_data_rows.txt"
    processor.process(file_name)
    print("\noutput dataframe")
    assert processor.df["LONGITUDE"].iloc(0)[0] == "120.4139"
    assert processor.df["LATITUDE"].iloc(0)[0] == "15.68754167"
    

if __name__ == "__main__":
    main()