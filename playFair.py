def prepare_text(text):
  # Remove non-alphabetic characters and convert to uppercase
  text = ''.join(filter(str.isalpha, text.upper()))
  # Replace 'J' with 'I' (Playfair does not use 'J')
  text = text.replace('J', 'I')
  return text


def generate_key_square(key):
  key = prepare_text(key)
  key_square = ''
  for char in key:
    if char not in key_square:
      key_square += char
  for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
    if char not in key_square:
      key_square += char
  return key_square


def find_position(key_square, letter):
  row = col = 0
  for i in range(5):
    for j in range(5):
      if key_square[i * 5 + j] == letter:
        row, col = i, j
        break
  return row, col


def playfair_encrypt(text, key):
  key_square = generate_key_square(key)
  text = prepare_text(text)

  # Handle double letters by inserting a filler character (e.g., 'X')
  i = 0
  while i < len(text) - 1:
    if text[i] == text[i + 1]:
      text = text[:i + 1] + 'X' + text[i + 1:]
    i += 2

  # Encrypt pairs of letters
  ciphertext = ''
  for i in range(1, len(text), 2):
    a, b = text[i - 1], text[i]
    row_a, col_a = find_position(key_square, a)
    row_b, col_b = find_position(key_square, b)

    if row_a == row_b:
      ciphertext += key_square[row_a * 5 +
                               (col_a + 1) % 5] + key_square[row_b * 5 +
                                                             (col_b + 1) % 5]
    elif col_a == col_b:
      ciphertext += key_square[((row_a + 1) % 5) * 5 + col_a] + key_square[(
          (row_b + 1) % 5) * 5 + col_b]
    else:
      ciphertext += key_square[row_a * 5 + col_b] + key_square[row_b * 5 +
                                                               col_a]

  return ciphertext


def playfair_decrypt(ciphertext, key):
  key_square = generate_key_square(key)

  plaintext = ''
  for i in range(1, len(ciphertext), 2):
    a, b = ciphertext[i - 1], ciphertext[i]
    row_a, col_a = find_position(key_square, a)
    row_b, col_b = find_position(key_square, b)

    if row_a == row_b:
      plaintext += key_square[row_a * 5 +
                              (col_a - 1) % 5] + key_square[row_b * 5 +
                                                            (col_b - 1) % 5]
    elif col_a == col_b:
      plaintext += key_square[((row_a - 1) % 5) * 5 + col_a] + key_square[(
          (row_b - 1) % 5) * 5 + col_b]
    else:
      plaintext += key_square[row_a * 5 + col_b] + key_square[row_b * 5 +
                                                              col_a]

  return plaintext
