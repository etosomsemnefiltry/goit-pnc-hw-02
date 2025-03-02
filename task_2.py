""" Шифр перестановки: """

def get_permutation_order(key):
    """
    Определяет порядок перестановки столбцов на основе ключа
    """
    return sorted(range(len(key)), key=lambda x: key[x])

def encrypt_transposition(text, key):
    """
    Шифрование методом простой перестановки
    """
    key_order = get_permutation_order(key)
    num_cols = len(key)
    num_rows = -(-len(text) // num_cols)  # Округление вверх
    
    # Заполняем таблицу
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    idx = 0
    for r in range(num_rows):
        for c in range(num_cols):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
            else:
                grid[r][c] = ' '  # Заполняем пробелами, если текст закончился
    
    # Читаем по столбцам согласно порядку
    cipher_text = ''
    for col in key_order:
        for row in range(num_rows):
            cipher_text += grid[row][col]
    
    return cipher_text

def decrypt_transposition(cipher_text, key):
    """
    Дешифрование методом простой перестановки
    """
    key_order = get_permutation_order(key)
    num_cols = len(key)
    num_rows = -(-len(cipher_text) // num_cols)
    
    # Создаем пустую таблицу
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    # Восстанавливаем порядок столбцов
    sorted_key_order = sorted(range(len(key)), key=lambda x: key[x])
    inverse_key_order = {sorted_key_order[i]: i for i in range(len(key))}
    
    # Заполняем столбцы в правильном порядке
    idx = 0
    for col in sorted(range(len(key)), key=lambda x: inverse_key_order[x]):
        for row in range(num_rows):
            if idx < len(cipher_text):
                grid[row][col] = cipher_text[idx]
                idx += 1
    
    # Читаем построчно
    plain_text = ''.join(''.join(row) for row in grid)
    
    return plain_text.strip()

def double_transposition_encrypt(text, key1, key2):
    """
    Двойное шифрование методом перестановки
    """
    first_pass = encrypt_transposition(text, key1)
    second_pass = encrypt_transposition(first_pass, key2)
    return second_pass

def double_transposition_decrypt(cipher_text, key1, key2):
    """
    Двойное дешифрование методом перестановки
    """
    first_pass = decrypt_transposition(cipher_text, key2)
    second_pass = decrypt_transposition(first_pass, key1)
    return second_pass

# Тестируем алгоритм
key1 = "SECRET"
key2 = "CRYPTO"
text = "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. The critic is he who can translate into another manner or a new material his impression of beautiful things. The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."

encrypted = encrypt_transposition(text, key1)
decrypted = decrypt_transposition(encrypted, key1)

double_encrypted = double_transposition_encrypt(text, key1, key2)
double_decrypted = double_transposition_decrypt(double_encrypted, key1, key2)

print(f"\n\nOriginal: {text}")
print(f"\n\nEncrypted (Single): {encrypted}")
print(f"\n\nDecrypted (Single): {decrypted}")

print(f"\n\nEncrypted (Double): {double_encrypted}")
print(f"\n\nDecrypted (Double): {double_decrypted}")