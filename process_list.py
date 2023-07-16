import pandas as pd
import re

COL_NAME = "NAME OF EVACUATION CENTER"
COL_ADDR = "ADDRESS"
COL_CAP = "INDIVIDUAL CAPACITY"
COL_LAT = "LATITUDE"
COL_LONG = "LONGITUDE"
COL_REMAIN = "UNPROCESSED WORDS"

OUTPUT_FILE_NAME = "new_list.csv"

def main():
    # import the file to be used
    file_dir = "list_evac_center_garie.txt"
    with open(file_dir, "r", encoding="utf-8") as file:
        reader = file.readlines()
        # initialize an empty list where dictionaries of each row will be placed
        list_of_dict = []
        # iterate over each row of the csv file
        for row in reader:
            # some of the rows have no length (empty), try skips those
            if row != ""  or row != "\n":
                print(f"{repr(row)}")
                # initialize the string as empty
                string = ""
                # initialize the dictionary to be empty
                dictionary = dict.fromkeys([COL_NAME, COL_ADDR, COL_CAP, COL_LAT, COL_LONG])

                # flag whether a value was added to the dicitonary
                has_value = False
                # iterate through each character checking for conditions
                for i in range(len(row)):
                    BUFFER = 5
                    string += row[i]
                    string_buffer = row[i+1:i+BUFFER+1]
                    # check if next 5 characters in string is either "Brgy" or "Bray"
                    if is_brgy_bray(string_buffer):
                        # append the string to a dictionary as "NAME OF EVACUATION CENTER"
                        dictionary[COL_NAME] = string.strip()
                        has_value = True
                        string = ""
                    # check if next 5 characters in string is either " ## " or "### "
                    elif is_capacity_next(string_buffer):
                        # append the string to a dicitonary as "ADDRESS"
                        dictionary[COL_ADDR] = string.strip()
                        has_value = True
                        string = ""
                    # check if next 5 characters in string is "##.##"
                    elif is_latitude_next(string_buffer):
                        print(f"Capacity: {string}, activated by {string_buffer}")
                        # append the string to a dictionary as "INDIVIDUAL CAPACITY"
                        dictionary[COL_CAP] = string.strip()
                        has_value = True
                        string = ""
                    # check if next 5 characters in string is "###.#"
                    elif is_longitude_next(string):
                        # append the string to a dictionary as "LATITUDE"
                        dictionary[COL_LAT] = string.strip()
                        print(f"Latitude: {dictionary[COL_LAT]}, activated by {repr(string_buffer)}")
                        has_value = True
                        string = ""
                    # append the remaining string to a dictionary as "LONGITUDE"
                    elif (dictionary[COL_LAT] != None):
                        dictionary[COL_LONG] = string.strip()
                        print(f"Longitude:\"{dictionary[COL_LONG]}\"")
                # append dictionary to list if not empty
                if has_value:
                    list_of_dict.append(dictionary)

        df = pd.DataFrame(list_of_dict)
    print(list_of_dict)
    print(df[[COL_NAME,COL_LAT,COL_LONG]].head(3))
    print(df[[COL_LAT,COL_LONG]].tail(3))
    df.to_csv(OUTPUT_FILE_NAME)
    # write_df_to_csv(df=df, file_name=FILE_NAME[:-4], iteration=0)

class evac_list_processor():
    """This class encompasses all the functionality for converting
    a text document into a dataframe and exporting that"""

    def __init__(self) -> None:
        pass

def is_brgy_bray(string:str)-> bool:
    """check characters in string is either "Brgy" or "Bray" """
    REGEX = r"Br[ga]y."
    return re.search(REGEX, string) != None

def is_capacity_next(string:str)-> bool:
    """check characters in string is either " ## " or "### " """
    REGEX1 = r"[^\S\r\n][0-9]{2}[^\S\r\n]."
    REGEX2 = r"[^\S\r\n][0-9]{3}[^\S\r\n]"
    return (re.search(REGEX1, string) != None) or (re.search(REGEX2, string) != None)

def is_latitude_next(string:str)-> bool:
    """check if characters in string is "##.##" """
    REGEX = r"15[.,][0-9]{2}"
    return re.search(REGEX, string) != None

def is_longitude_next(string:str)-> bool:
    """check if characters in string is "###.#" """
    REGEX = r"120[.,][0-9]"
    REGEX_EXCEPT = r"^[\n]"
    return (re.search(REGEX, string) != None) and (re.search(REGEX_EXCEPT, string) == None)
    
def is_at_end(string:str)-> bool:
    """check if it is the last character for the row \n """
    REGEX = r"[0-9]{4}[\n]"
    return re.search(REGEX, string) != None

def clean_number(string:str)-> str:
    """this function takes a string of numbers, and removes any
    characters that are neither numeric nor a period while converting
    commas into periods"""
    pass

def write_df_to_csv(df:pd.DataFrame, file_name:str, iteration:int)-> None:
    """This function attempts to use the to_csv method of a dataframe.
    If an exception is raised, that might mean that there is an existing
    file in use under that name, then the function attempts to write the
    file to modify the name until it either reaches its limit or it does
    not encounter an error."""
    
    # set the limitation on the iteration
    ITER_LIMIT = 5
    
    # try the to_csv method of the dataframe
    try:
        df.to_csv(file_name + ".csv")
    except:
        if iteration < 5:
            iteration += 1
            print(iteration)
            write_df_to_csv(df, file_name, iteration)
        else:
            pass


if __name__ == "__main__":
    main()