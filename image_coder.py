from PIL import Image, ImageDraw
from fun_image_coder import _get_fixet_for_str, _convert_str_to_bin, _decoder_bin_to_str

class ImageC():
    # Для поддержки кирилицы block_size=12
    # Для поддержки всей таблицы ASCII block_size=16
    def __init__(self, path, block_size=8):
        self._path = path
        self._image = Image.open(path)
        self._block_size = block_size
        self.width = self._image.width
        self.height = self._image.height
        self._container_size = int((int(self.width) + int(self.height)) * 3 / self._block_size)

    def info(self):
        print(f'{self.width} x {self.height}')
        print(f'Max lenth mesege : {self._container_size}')

    # Разворачивает всю RGB матрицу пикселей в один длтнный одномерный список
    def _unpack_pixs_obj(self):
        pixels = self._image.load()
        pixs_list = list()
        for x in range(self.width):
            for y in range(self.height):
                r = pixels[x, y][0]
                g = pixels[x, y][1]
                b = pixels[x, y][2]
                pixs_list += [r, g, b]

        return pixs_list

    # Вносит изменения в палитру RGB согласно свернутой матрице
    def _pack_and_draw(self, input_list):
        ls = input_list
        drw = ImageDraw.Draw(self._image)
        index = 0
        for x in range(self.width):
            for y in range(self.height):
                r = ls[index]
                g = ls[index + 1]
                b = ls[index + 2]

                drw.point((x, y), (r, g, b))
                index += 3
        del drw

    # Кодирование сообщения по ключу в развернутую RGB матрицу пикселей
    def encoding_mesege(self, message, key):
        if len(message) < self._container_size:
            key_normal_size = _get_fixet_for_str(key, len(message))
            key_bin = _convert_str_to_bin(key_normal_size, block_size=self._block_size)
            message_bin = _convert_str_to_bin(message, block_size=self._block_size)
            pixel_list = list(self._unpack_pixs_obj())
            l_rem = lambda x: x - 1

            # делаем все необходимые для записи сообщения значения четными + последовательность "0"*размер блока данных
            for _ in range(len(message_bin) + self._block_size):
                pixel_list[_] = pixel_list[_] if pixel_list[_] % 2 == 0 else l_rem(pixel_list[_])

            # вносим изменения в развернутый список пикселей
            for index in range(len(message_bin)):
                coef = int(message_bin[index]) ^ int(key_bin[index])
                if coef == 1:
                    pixel_list[index] += coef
            self._pack_and_draw(pixel_list)
            return pixel_list

    # Декодирует матрицу по ключу
    def decoding_image(self, key):
        pixels_ls = self._unpack_pixs_obj()
        blocks = []
        block = ''
        for item in pixels_ls:
            if item % 2 == 0:
                block += '0'
            else:
                block += '1'
            if len(block) == self._block_size:
                if not block == '0' * self._block_size:
                    blocks.append(block)
                    block = ''
                else:
                    break
        if not blocks:
            raise ('No cripted massage')
        key_len = len(blocks)
        blocks = ''.join(blocks)
        full_key = _get_fixet_for_str(key, key_len)
        full_key_bin = _convert_str_to_bin(full_key, block_size=self._block_size)
        decoder_bin = ''
        for index in range(len(blocks)):
            b_int = int(blocks[index])
            k_int = int(full_key_bin[index])
            decoder_bin += str(b_int ^ k_int)
        decoder_str = _decoder_bin_to_str(decoder_bin, LEN_BLOCK=self._block_size)
        return decoder_str

    # Сохранеине, изза особенностей сжатия JPEG формата в нем не выходт сохранить измененную матрицу
    def save(self, path, format):
        self._image.save(path, format)


image_jpg = ImageC('img.jpg')
image_jpg.info()
image_jpg.encoding_mesege('Secret text in JPG file','Secret key from JPG')
image_jpg.save('c_img_jpg.png','PNG')

image_png = ImageC('img.png')
image_png.info()
image_png.encoding_mesege('Secret text in PNG file','Secret key from PNG')
image_png.save('c_img_png.png','PNG')


c_img_jpg = ImageC('c_img_jpg.png')
print(c_img_jpg.decoding_image('Secret key from JPG'))

c_img_png = ImageC('c_img_png.png')
print(c_img_png.decoding_image('Secret key from PNG'))
