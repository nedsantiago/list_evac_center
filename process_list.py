import pandas as pd
from re import search, sub

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
    processor = evac_list_processor()
    processor.process(file_dir)
    processor.df.to_csv("new_list.csv")

class evac_list_processor():
    """This class encompasses all the functionality for converting
    a text document into a dataframe and exporting that"""

    def process(self, file_dir) -> None:
        with open(file_dir, "r", encoding="utf-8") as file:
            reader = file.readlines()
            # initialize an empty list where dictionaries of each row will be placed
            list_of_dict = []
            # iterate over each row of the csv file
            for row in reader:
                # some of the rows have no length (empty), try skips those
                if row != ""  or row != "\n":
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
                        if self.is_brgy_bray(string_buffer):
                            # append the string to a dictionary as "NAME OF EVACUATION CENTER"
                            dictionary[COL_NAME] = string.strip()
                            has_value = True
                            string = ""
                        # check if next 5 characters in string is either " ## " or "### "
                        elif self.is_capacity_next(string_buffer):
                            # append the string to a dicitonary as "ADDRESS"
                            dictionary[COL_ADDR] = string.strip()
                            has_value = True
                            string = ""
                        # check if next 5 characters in string is "##.##"
                        elif self.is_latitude_next(string_buffer):
                            # append the string to a dictionary as "INDIVIDUAL CAPACITY"
                            dictionary[COL_CAP] = string.strip()
                            has_value = True
                            string = ""
                        # check if next 5 characters in string is "###.#"
                        elif self.is_longitude_next(string_buffer):
                            # append the string to a dictionary as "LATITUDE"
                            string = self.clean_number(string=string)
                            dictionary[COL_LAT] = string.strip()
                            has_value = True
                            string = ""
                        # append the remaining string to a dictionary as "LONGITUDE"
                        elif (dictionary[COL_LAT] != None):
                            string = self.clean_number(string=string)
                            dictionary[COL_LONG] = string.strip()
                    # append dictionary to list if not empty
                    if has_value:
                        list_of_dict.append(dictionary)

            df = pd.DataFrame(list_of_dict)
            self.df = df
        print(list_of_dict)
        print(df[[COL_NAME,COL_LAT,COL_LONG]].head(3))
        print(df[[COL_LAT,COL_LONG]].tail(3))

    def is_brgy_bray(self, string:str)-> bool:
        """check characters in string is either "Brgy" or "Bray" """
        REGEX = r"Br[ga]y."
        return search(REGEX, string) != None

    def is_capacity_next(self, string:str)-> bool:
        """check characters in string is either " ## " or "### " """
        REGEX1 = r"[^\S\r\n][0-9]{2}[^\S\r\n]."
        REGEX2 = r"[^\S\r\n][0-9]{3}[^\S\r\n]"
        return (search(REGEX1, string) != None) or (search(REGEX2, string) != None)

    def is_latitude_next(self, string:str)-> bool:
        """check if characters in string is "15.##" """
        REGEX = r"15[.,][0-9]{2}"
        return search(REGEX, string) != None

    def is_longitude_next(self, string:str)-> bool:
        """check if characters in string is "120.#" """
        REGEX = r"120[.,][0-9]"
        return search(REGEX, string) != None
        
    def is_at_end(self, string:str)-> bool:
        """check if it is the last character for the row \n """
        REGEX = r"[0-9]{4}[\n]"
        return search(REGEX, string) != None

    def clean_number(self, string:str)-> str:
        """this function takes a string of numbers, and removes any
        characters that are neither numeric nor a period while converting
        commas into periods"""

        REGEX1 = r"[|]"
        string = sub(REGEX1, r"", string=string)
        REGEX2 = r","
        string = sub(REGEX2, r".", string=string)
        return string

if __name__ == "__main__":
    main()