import re

# Display the list of categories and ask the user to select one
def select_category(categories):

    print("Select a category:")
    for i, category in enumerate(categories):
        print(f"{i+1}. {category}")

    # Get the user's selection
    while True:
        try:
            user_input = int(input("Enter the serial number of your selection: "))
            if 1 <= user_input <= len(categories):
                break
            else:
                print("Invalid selection. Please enter a number between 1 and", len(categories))
        except ValueError:
            print("Invalid input. Please enter a number.")

    return categories[user_input-1]


def generate_uuid():
  import uuid
  guuid = uuid.uuid4()
  guuid = str(guuid).replace('-', '')         
  #  to strip only leading non-aplha characters
  return guuid
   
def strip_non_alphanumeric_leading(s):
#  to strip only leading non-aplha characters
   return re.sub(r'^[^a-zA-Z0-9]+', '', s)

def strip_non_alphanumeric(s):
#  to strip leading and trailing
   return re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', s)


