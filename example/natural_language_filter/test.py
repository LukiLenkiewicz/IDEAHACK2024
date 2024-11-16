# %%
from sentence_transformers import SentenceTransformer
from ideahack.profile_store import ProfileStoreHandler
from ideahack.nls.vector_store import VectorStoreHandler
from ideahack.nls.search_engine import HybridSearchSystem

# Initialize SentenceTransformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize VectorStoreHandler
vector_store_handler = VectorStoreHandler(vector_store_file='vector_store.index')

# Initialize ProfileStoreHandler
profile_store_handler = ProfileStoreHandler(sentence_model=sentence_model, metadata_db_file='metadata.db')

# %%
# Add a sample user profile
user_profile_data = {
    'name': 'John',
    'surname': 'Doe',
    'email': 'johndoe@example.com',
    'bio': 'Experienced data scientist with a focus on machine learning and AI.',
    'experience': '5 years working in AI and machine learning projects.',
    'skills': ['Python', 'Machine Learning', 'Deep Learning'],
    'link': 'https://johndoe.com',
    'type': 'Developer',
}

# Add the user profile to the database
profile_store_handler.add_user_profile(user_profile_data, vector_store_handler)

# Add a sample company profile
company_profile_data = {
    'name': 'Tech Innovators Inc.',
    'email': 'contact@techinnovators.com',
    'bio': 'Leading company in AI and Machine Learning solutions and software development.',
    'services': ['AI Development', 'Software Consulting'],
    'link': 'https://techinnovators.com',
    'location': 'San Francisco, CA',
}

# Add the company profile to the database
profile_store_handler.add_company_profile(company_profile_data, vector_store_handler)

# %%
# Initialize HybridSearchSystem
search_system = HybridSearchSystem(filters_file='filters.json', vector_store_handler=vector_store_handler, profile_store_handler=profile_store_handler, sentence_model=sentence_model)

# Perform a search query
search_query = 'Looking for a company that specializes in Machine Learning.'
results = search_system.hybrid_search(search_query)

# Display search results
for result in results:
    print(result)


