import sys

def valid_size(size:int, lower:int, upper:int) -> bool:
    return True if size >= lower and size <= upper else False

def get_input(prompt:str = "", lower:int = 0, upper:int = sys.maxsize) -> int:
    response: int = 0;
    while (not valid_size(size=response, lower=lower, upper=upper)):
        try:
            response = int(input(prompt))
            if (not valid_size(size=response, lower=lower, upper=upper)):
                print(f"Invalid input for range {lower} to {upper}.")
        except:
            print("Invalid input, not a number.")
    
    return response