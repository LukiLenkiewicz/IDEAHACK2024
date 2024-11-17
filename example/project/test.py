# %%
from ideahack.project.generator import PitchDeckGenerator

# %%
project_info = {
    "name": "Plastic Recycling",
    "bio": "An innovative solution for recycling plastic into construction material",
    "area_of_research": "Material Science",
    "cost_structure": "500000"
}

generator = PitchDeckGenerator('g_slides.json')
id, pitch_deck_dict = generator.generate_and_create_pitch_deck(project_info, 'PitchDeck')

# %%
presentation_link = generator.generate_presentation_link(id)
print(f"View the presentation here: {presentation_link}")
presentation_pdf = "Recycling_Innovation_Pitch_Deck.pdf"
generator.download_presentation_as_pdf(id, presentation_pdf)