from wordcloud import WordCloud, STOPWORDS
import string
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st
import io
import pandas as pd
import docx2txt
import re


def make_wordcloud(text_input, filename="wordcloud.png"):
    stopwords = set(STOPWORDS)
    tokens = text_input.split()
    punctuation_mapping_table = str.maketrans('', '', string.punctuation)
    tokens_stripped_of_punctuation = [token.translate(punctuation_mapping_table)
                                  for token in tokens]
    lower_tokens = [token.lower() for token in tokens_stripped_of_punctuation]

    joined_string = (" ").join(lower_tokens)

    wordcloud = WordCloud(width=1800,
                      height=1800,
                      stopwords=stopwords,
                      min_font_size=20).generate(joined_string)

    plt.figure(figsize=(30,40))
    # Turn off axes
    plt.axis("off")
    # Display (essential to actually get the wordcloud in the image)
    plt.imshow(wordcloud)
    # Save the wordcloud to a file
    plt.savefig(filename)


def make_wordcloud_with_image_mask(
        text_input,
        filename="wordcloud.png",
        mask_image=None,
        custom_stopwords="",
        **kwargs
        ):
    combined_stopwords = STOPWORDS.union(custom_stopwords)
    stopwords = set(combined_stopwords)
    
    tokens = text_input.split()
    punctuation_mapping_table = str.maketrans('', '', string.punctuation)
    tokens_stripped_of_punctuation = [token.translate(punctuation_mapping_table)
                                  for token in tokens]
    lower_tokens = [token.lower() for token in tokens_stripped_of_punctuation]

    joined_string = (" ").join(lower_tokens)

    plt.figure(figsize=(30,40))
    plt.axis("off")

    if mask_image is not None:
        mask_image_opened = Image.open(mask_image)
        mask_array = np.array(mask_image_opened)

        wordcloud = WordCloud(width=mask_array.shape[1],
                    height=mask_array.shape[0],
                    stopwords=stopwords,
                    mask=mask_array,
                    **kwargs).generate(joined_string)

        plt.imshow(wordcloud, interpolation='bilinear')

    else:
        wordcloud = WordCloud(width=1800,
                    height=1800,
                    stopwords=stopwords,
                    **kwargs).generate(joined_string)

        plt.imshow(wordcloud)

    plt.savefig(filename)
    return wordcloud.to_image()



penguin_text = """
Penguins are a group of aquatic flightless birds from the family Spheniscidae
of the order Sphenisciformes.
They live almost exclusively in the Southern Hemisphere: only one species,
the Galapagos penguin, is found north of the Equator. Highly adapted for life in the ocean water,
penguins have countershaded dark and white plumage and flippers for swimming. Most penguins feed
on krill, fish, squid and other forms of sea life which they catch with their bills and swallow
whole while swimming. A penguin has a spiny tongue and powerful jaws to grip slippery prey.

They spend about half of their lives on land and the other half in the sea.
The largest living species is the emperor penguin (Aptenodytes forsteri):
on average, adults are about 1.1 m (3 ft 7 in) tall and weigh 35 kg (77 lb).
The smallest penguin species is the little blue penguin (Eudyptula minor),
also known as the fairy penguin, which stands around 30–33 cm (12–13 in) tall and
weighs 1.2–1.3 kg (2.6–2.9 lb).
Today, larger penguins generally inhabit colder regions, and smaller penguins inhabit regions
with temperate or tropical climates. Some prehistoric penguin species were enormous:
as tall or heavy as an adult human.There was a great diversity of species in subantarctic regions,
and at least one giant species in a region around 2,000 km south of the equator 35 mya, during
the Late Eocene, a climate decidedly warmer than today.
"""

st.title("Word Cloud")
input_text = st.text_area("Input Word Cloud Text",height=250,value=penguin_text)
#color_scheme = st.text_input("Input Word Cloud Colour Scheme",value = 'viridis')
color_options = ['viridis','Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']
color_scheme = st.selectbox("Choose an option", color_options)
#background_color = st.text_input("Input Word Cloud Background Colour",value = 'None')
background_color_options = ['black','red','pink','yellow','blue','orange','purple','white']
background_color = st.selectbox("Choose an option", background_color_options)
txt_size = st.number_input("Minimum Input Word Cloud Text Size",value = 6)
custom_stopword = st.text_area("Input Words to Exclude",height=50,value="")
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
uploaded_file = st.file_uploader("Choose a file...", type=["txt", "csv", "doc","docx"])
#WordCloud()

if uploaded_file:
    if uploaded_file.type == "text/plain":
        # Read the text file
        input_text = uploaded_file.read().decode("utf-8")
        
    elif uploaded_file.type == "text/csv":
        # Read the CSV file
        input_text = pd.read_csv(uploaded_file)


    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                                  "application/msword"]:
        input_text = docx2txt.process(uploaded_file)

if custom_stopword:
    #stopword_list = [word.strip() for word in custom_stopword.split(',')]
    stopword_list = [word.strip() for word in re.split(r'[,\s]+', custom_stopword) if word]
else:
    stopword_list = []



if input_text:
    st.write(input_text)
    # make_wordcloud(input_text)
    # image = Image.open("wordcloud.png")
    # st.image(image, caption='Generated Word Cloud')

    
    # make_wordcloud_with_image_mask(input_text,"wordcloud2.png",
    #     min_font_size=txt_size,colormap=color_scheme,
    #     background_color=background_color, custom_stopwords=custom_stopword)
    # image2 = Image.open("wordcloud2.png")
    # st.image(image2, caption='Generated Word Cloud')
    cloud = make_wordcloud_with_image_mask(input_text,"wordcloud2.png",
        min_font_size=txt_size,colormap=color_scheme,
        background_color=background_color, custom_stopwords=stopword_list,
        mask_image = uploaded_image
        )
    st.image(cloud, caption='Generated Word Cloud')
    with open("wordcloud2.png", "rb") as file:
        st.download_button(label="Download Word Cloud",
            data=file,
            file_name="wordcloud2.png",mime="image/png")

