import hashlib

LEN_BLOCK = 14


# Принимает цело число типа int(от 0 до 65 535(при LEN_BLOCK=16(поддерживает все языки и все спецсимволы из таблицы ASCII))) и преобразует в 16 значный код вида (101101..)
# Бинарное представление числа
def _fix_len_bine(int_value,LEN_BLOCK=LEN_BLOCK):
    str_bin = bin(int_value)[2:]
    str_bin = str_bin.zfill(LEN_BLOCK)
    return str_bin


# Преобразует строку символов из n char в строку символов(001010101....) размерностью n*LEN_BLOCK
def _convert_str_to_bin(str_obj,block_size = LEN_BLOCK):
    _bin = ''
    for char in str_obj:
        _ascii_convert = (ord(char))
        _bin_chr = _fix_len_bine(_ascii_convert,LEN_BLOCK=block_size)
        _bin += _bin_chr
    return _bin


# Функция обратная _convert_str_to_bin
def _decoder_bin_to_str(bin_str,LEN_BLOCK = LEN_BLOCK):
    all_char = []
    str_out = ""
    block = ''
    for item in bin_str:
        if len(block) < LEN_BLOCK:
            block += item
        else:
            all_char.append(block)
            block = item
    else:
        all_char.append(block)

    for char in all_char:
        if len(char) != 0:
            str_out += chr(int(char, 2))
    return str_out


# Принимает ключ(для кодирования) и необходиму длинну последовательности
# возвращает строку длинной need_lean уникальных комбинаций
# _get_fixet_for_str('Какойто ключ',20)
# вывод : str('0627ff4efbc89c0b00c3')
def _get_fixet_for_str(str_obj, need_lean):
    hash_obj = hashlib.md5(str_obj.encode('utf-8')).hexdigest()
    if len(hash_obj) >= need_lean:
        return hash_obj[:need_lean]
    elif len(hash_obj) < need_lean:
        while len(hash_obj) < need_lean:
            new_hash = hashlib.md5(hash_obj.encode('utf-8')).hexdigest()
            hash_obj += new_hash
        return hash_obj[:need_lean]


# Кодирует
# на фход принимает строку для кодирования и строку ключ произвольной длинны
def _cripto(str_object, key):
    key_hash = _get_fixet_for_str(key, len(str_object))

    # приводим слово и ключ к виду 0 и 1
    bin_str = _convert_str_to_bin(str_object)
    bin_key_hash = _convert_str_to_bin(key_hash)
    bin_out = ''
    for index in range(len(bin_key_hash)):
        bin_out += str(int(bin_str[index]) ^ int(bin_key_hash[index]))
    str_out = _decoder_bin_to_str(bin_out)
    return str_out


# Декодирует
# на фход принимает закодированную строку и строку ключ произвольной длинны
def _encript(str_obj, key):
    return _cripto(str_obj, key)



