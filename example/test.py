# %%
from ideahack.virtual_sibling.interact import VirtualSibling

# %%
# User enters some profile - the information is retrieved and VirtualSibling is initialized
current_profile_id = 1
current_profile_type = 'user'
virtual_sibling = VirtualSibling(current_profile_id, current_profile_type, db_path='virtual_sibling.db')

# %%
print("Profile data:")
print(virtual_sibling.profile_data)

# %%
while True:
    user_query = input("Ask a question: ")
    if user_query == "exit":
        break
    response = virtual_sibling.query(user_query)
    print("Response:")
    print(response)


