# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
import streamlit as st
from PIL import Image

from playFair import playfair_encrypt
from playFair import playfair_decrypt

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
import streamlit as st

#modify this code into a streamlit app
st.set_page_config(page_title="cipherShroud")
st.markdown("<h1 style='text-align: center; color: white;'>cipherShroud</h1>",
            unsafe_allow_html=True)


def encode_img(img1, img2):
  img1_pixels = img1.load()
  img2_pixels = img2.load()
  cover_up = Image.new('RGB', (img1.width, img1.height), 'black')
  cover_up_pixels = cover_up.load()

  for x in range(0, cover_up.width):
    for y in range(0, cover_up.height):
      br, bg, bb = img1_pixels[x, y]
      ar, ag, ab = img2_pixels[x, y]

      # first 4 bytes from cover up (msb) +  first 4 bytes of secret
      cr = int(f'{br:08b}'[:4] + f'{ar:08b}'[:4], 2)
      cg = int(f'{bg:08b}'[:4] + f'{ag:08b}'[:4], 2)
      cb = int(f'{bb:08b}'[:4] + f'{ab:08b}'[:4], 2)

      cover_up_pixels[x, y] = (cr, cg, cb)
  new_img_name = st.text_input("Enter name of stego image(with extension) :")
  cover_up.save(new_img_name, str(new_img_name.split(".")[1].upper()))

  return cover_up, new_img_name


def decode_img(cover_up):
  cover_up_pixels = cover_up.load()
  secret = Image.new('RGB', (cover_up.width, cover_up.height), 'black')
  secret_pixels = secret.load()

  for x in range(0, secret.width):
    for y in range(0, secret.height):
      r, g, b = cover_up_pixels[x, y]

      sr = int(f'{r:08b}'[4:] + '0000', 2)
      sg = int(f'{g:08b}'[4:] + '0000', 2)
      sb = int(f'{b:08b}'[4:] + '0000', 2)

      secret_pixels[x, y] = (sr, sg, sb)
  return secret


def genData(data):

  # list of binary codes
  # of given data
  newd = []

  for i in data:
    newd.append(format(ord(i), '08b'))
  return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

  datalist = genData(data)
  lendata = len(datalist)
  imdata = iter(pix)

  for i in range(lendata):

    # Extracting 3 pixels at a time
    pix = [
        value for value in imdata.__next__()[:3] + imdata.__next__()[:3] +
        imdata.__next__()[:3]
    ]

    # Pixel value should be made
    # odd for 1 and even for 0
    for j in range(0, 8):
      if (datalist[i][j] == '0' and pix[j] % 2 != 0):
        pix[j] -= 1

      elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
        if (pix[j] != 0):
          pix[j] -= 1
        else:
          pix[j] += 1
        # pix[j] -= 1

    # Eighth pixel of every set tells
    # whether to stop ot read further.
    # 0 means keep reading; 1 means thec
    # message is over.
    if (i == lendata - 1):
      if (pix[-1] % 2 == 0):
        if (pix[-1] != 0):
          pix[-1] -= 1
        else:
          pix[-1] += 1

    else:
      if (pix[-1] % 2 != 0):
        pix[-1] -= 1

    pix = tuple(pix)
    yield pix[0:3]
    yield pix[3:6]
    yield pix[6:9]


def encode_enc(newimg, data):
  w = newimg.size[0]
  (x, y) = (0, 0)

  for pixel in modPix(newimg.getdata(), data):

    # Putting modified pixels in the new image
    newimg.putpixel((x, y), pixel)
    if (x == w - 1):
      x = 0
      y += 1
    else:
      x += 1


# Encode data into image
def encode(image):
  data = st.text_input("Enter the text to be hidden"
                       )  # Input the text to be hidden from the user
  #img = input("Enter image name(with extension) : ")
  #image = Image.open(img, 'r')

  #data = input("Enter data to be encoded : ")
  # if (len(data) == 0):
  #   raise ValueError('Data is empty')

  newimg = image.copy()
  key = 'stegano'

  ciphertext = playfair_encrypt(data, key)
  #ciphertext=ciphertext.encode()
  encode_enc(newimg, ciphertext)

  new_img_name = st.text_input("Enter name of stego image(with extension) :")
  newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

  return newimg, new_img_name


# Decode the data in the image
def decode(image):
  # data = st.text_input("Enter the text to be hidden")
  # img = input("Enter image name(with extension) : ")
  # image = Image.open(img, 'r')

  data = ''
  imgdata = iter(image.getdata())

  while (True):
    pixels = [
        value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] +
        imgdata.__next__()[:3]
    ]

    # string of binary data
    binstr = ''

    for i in pixels[:8]:
      if (i % 2 == 0):
        binstr += '0'
      else:
        binstr += '1'

    data += chr(int(binstr, 2))
    key = 'stegano'
    data1 = playfair_decrypt(data, key)
    if (pixels[-1] % 2 != 0):
      return data1


footer = """<style>
a:link , a:visited{
color: whites;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: white;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="https:///" target="_blank">Team cipherShroud</a></p>
</div>
"""


# Main Function
def main():
  # Streamlit UI

  option = st.selectbox(
      'Choose an action',
      ('Encode', 'Decode'))  # Ask the user to choose either encode or decode

  if option == 'Encode':
    uploaded_file = st.file_uploader(
        "Choose a cover image",
        key='cover_image')  # Input a file from the file browser from the user

    if uploaded_file is not None:
      image = Image.open(uploaded_file)
      option = st.selectbox('Choose Stego type', ('Hide Image', 'Hide Text'))

      if option == 'Hide Image':
        #logic for hiding image in image
        # Ask the user to choose either encode or decode
        st.image(image, caption='Uploaded Cover Image.', use_column_width=True)
        uploaded_file = st.file_uploader(
            "Choose an image to hide", key='hide_image'
        )  # Input a file from the file browser from the user
        if uploaded_file is not None:
          imageHide = Image.open(uploaded_file)
          st.image(imageHide, caption='Image to hide.', use_column_width=True)

          stego_img, new_img_name = encode_img(image, imageHide)
          if st.button('Encode'):
            st.image(stego_img, caption='Stego Image.', use_column_width=True)
          if new_img_name:
            with open(new_img_name, "rb") as file:
              btn = st.download_button(label="Download Stego image",
                                       data=file,
                                       file_name=new_img_name,
                                       mime="image/png")

      elif option == 'Hide Text':
        #logic for hiding text in image
        st.image(image, caption='Uploaded Cover Image.', use_column_width=True)
        newimg, new_img_name = encode(image)
        if st.button('Encode'):
          st.image(newimg, caption='New Stego Image.',
                   use_column_width=True)  # Display the new stego image
          if new_img_name:
            with open(new_img_name, "rb") as file:
              btn = st.download_button(label="Download Stego image",
                                       data=file,
                                       file_name=new_img_name,
                                       mime="image/png")

  elif option == 'Decode':
    uploaded_file = st.file_uploader(
        "Choose the Stego Image", key='image_to_decode'
    )  # Input a file from the file browser from the user

    image = None  # Initialize image variable

    if uploaded_file is not None:
      image = Image.open(uploaded_file)
    if image is not None:
      st.image(image, caption='Image to be decoded.', use_column_width=True)
    else:
      st.write('No image provided for decoding.')
    option = st.selectbox('Choose Stego type',
                          ('Extract Image', 'Extract Text'))
    if option == 'Extract Text':
      if st.button(
          'Decode') and image is not None:  # Check if image is not None
        decoded_data = decode(image)
        st.text('Decoded Text: ' + decoded_data)  # Display the decoded text
    elif option == 'Extract Image':
      if st.button('Decode') and image is not None:
        decoded_data = decode_img(image)
        st.image(decoded_data, caption='Decoded Image.', use_column_width=True)

  st.markdown(footer, unsafe_allow_html=True)


# Driver Code
if __name__ == '__main__':

  # Calling main function
  main()
