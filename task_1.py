from collections import Counter

""" Шифр Віженера: """

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENGLISH_FREQ = {'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 12.7, 'F': 2.2, 'G': 2.0, 'H': 6.1,
                'I': 6.7, 'J': 0.2, 'K': 0.8, 'L': 4.0, 'M': 2.4, 'N': 6.7, 'O': 7.5, 'P': 1.9,
                'Q': 0.1, 'R': 6.0, 'S': 6.3, 'T': 9.1, 'U': 2.8, 'V': 1.0, 'W': 2.4, 'X': 0.2,
                'Y': 2.0, 'Z': 0.1}

# Очистка текста от неалфавитных символов
def clean_text(text):
    return ''.join([char.upper() for char in text if char.upper() in ALPHABET])

# Шифрование Виженера
def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key_index = 0
    for char in plaintext:
        if char.upper() in ALPHABET:
            shift = ord(key[key_index % len(key)].upper()) - ord('A')
            if char.isupper():
                new_char = ALPHABET[(ord(char) - ord('A') + shift) % 26]
            else:
                new_char = ALPHABET[(ord(char.upper()) - ord('A') + shift) % 26].lower()
            ciphertext += new_char
            key_index += 1
        else:
            ciphertext += char  # Сохраняем пробелы и знаки препинания
    return ciphertext

# Дешифрование Виженера
def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key_index = 0
    for char in ciphertext:
        if char.upper() in ALPHABET:
            shift = ord(key[key_index % len(key)].upper()) - ord('A')
            if char.isupper():
                new_char = ALPHABET[(ord(char) - ord('A') - shift) % 26]
            else:
                new_char = ALPHABET[(ord(char.upper()) - ord('A') - shift) % 26].lower()
            plaintext += new_char
            key_index += 1
        else:
            plaintext += char  # Сохраняем пробелы и знаки препинания
    return plaintext

# Поиск повторяющихся последовательностей
def find_repeating_sequences(ciphertext, min_length=3):
    sequences = {}
    for i in range(len(ciphertext) - min_length):
        seq = ciphertext[i:i+min_length]
        for j in range(i+min_length, len(ciphertext)-min_length+1):
            if ciphertext[j:j+min_length] == seq:
                if seq not in sequences:
                    sequences[seq] = [i]
                sequences[seq].append(j)
    return sequences

# Вычисление возможных длин ключа
def calculate_possible_key_lengths(sequences):
    distances = []
    for seq, positions in sequences.items():
        if len(positions) > 1:
            for i in range(1, len(positions)):
                distances.append(positions[i] - positions[i-1])
    
    if not distances:
        return []
    
    factors = []
    for d in distances:
        for i in range(2, d + 1):
            if d % i == 0:
                factors.append(i)
    
    factor_counts = Counter(factors)
    most_common = [length for length, _ in factor_counts.most_common(5)]
    return most_common

# Метод Касиски
def kasiski_attack(ciphertext):
    sequences = find_repeating_sequences(ciphertext)
    key_lengths = calculate_possible_key_lengths(sequences)
    if key_lengths:
        return min(key_lengths, key=lambda x: abs(x - 12))  # 12 — средняя длина ключа Виженера
    return None

# Разбиение текста на группы
def split_text(ciphertext, key_length):
    groups = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        if char.upper() in ALPHABET:
            groups[i % key_length] += char.upper()
    return groups

# Частотный анализ
def frequency_analysis(text):
    counter = Counter(text)
    total = sum(counter.values())
    return {char: (count / total) * 100 for char, count in counter.items()}

# Оценка сдвига на основе частотного анализа
def guess_caesar_shift(group):
    freq = frequency_analysis(group)
    best_shift = 0
    best_score = float('-inf')
    for shift in range(26):
        score = 0
        for char in freq:
            shifted_char = ALPHABET[(ord(char) - ord('A') - shift) % 26]
            score += freq[char] * ENGLISH_FREQ.get(shifted_char, 0)
        if score > best_score:
            best_score = score
            best_shift = shift
    return best_shift

# Проверка правильности ключа на биграммах английского
def validate_key(ciphertext, key):
    decrypted = vigenere_decrypt(ciphertext, key)
    common_bigrams = ["TH", "HE", "IN", "ER", "AN", "RE", "ND"]
    score = sum(decrypted.upper().count(bigram) for bigram in common_bigrams)
    return score

# Восстановление ключа
def kasiski_recover_key(ciphertext, key_length):
    groups = split_text(ciphertext, key_length)
    possible_keys = []
    for group in groups:
        shift = guess_caesar_shift(group)
        key_char = ALPHABET[(26 - shift) % 26]
        possible_keys.append(key_char)
    
    best_key = "".join(possible_keys)
    return best_key if validate_key(ciphertext, best_key) > 5 else "UNKNOWN"

if __name__ == "__main__":
    plaintext = "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. The critic is he who can translate into another manner or a new material his impression of beautiful things. The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."
    key = "CRYPTOGRAPHY"
    
    # Очистка текста
    cleaned_plaintext = clean_text(plaintext)
    print("Очищенный текст:", cleaned_plaintext)
    
    # Шифрование
    ciphertext = vigenere_encrypt(cleaned_plaintext, key)
    print("Зашифрованный текст:", ciphertext)
    
    # Дешифрование с известным ключом
    decrypted_text = vigenere_decrypt(ciphertext, key)
    print("Дешифрованный текст:", decrypted_text)
    
    # Взлом методом Касиски
    estimated_key_length = kasiski_attack(ciphertext)
    print("Оцененная длина ключа:", estimated_key_length)
    
    if estimated_key_length:
        recovered_key = kasiski_recover_key(ciphertext, estimated_key_length)
        print("Восстановленный ключ:", recovered_key)
        decrypted_text_kasiski = vigenere_decrypt(ciphertext, recovered_key)
        print("Дешифрованный текст методом Касиски:", decrypted_text_kasiski)
    
    # Ручная проверка длины ключа (например, 12)
    manual_key_length = 12
    print(f"\nРучная проверка длины ключа: {manual_key_length}")
    recovered_key_manual = kasiski_recover_key(ciphertext, manual_key_length)
    print("Восстановленный ключ (ручная проверка):", recovered_key_manual)
    decrypted_text_manual = vigenere_decrypt(ciphertext, recovered_key_manual)
    print("Дешифрованный текст (ручная проверка):", decrypted_text_manual)