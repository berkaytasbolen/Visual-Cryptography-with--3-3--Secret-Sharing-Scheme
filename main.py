import cv2
import numpy as np
import random

def create_shares_3_3(img_binary):
    """
    (3,3) Görsel Şifreleme için üç pay (share) oluşturur.
    Her piksel, rastgele mantıksal işlemlerle paylara bölünür.
    """
    h, w = img_binary.shape
    shares = [np.zeros((h, w), dtype=np.uint8) for _ in range(3)]

    for i in range(h):
        for j in range(w):
            pixel = img_binary[i, j]
            if pixel == 0:  # Siyah piksel
                # Rastgele iki bit üret ve XOR ile üçüncü bit'i oluştur
                bit1 = random.randint(0, 1)
                bit2 = random.randint(0, 1)
                bit3 = bit1 ^ bit2  # XOR işlemi

                # Payları rastgele karıştırılmış siyah/beyaz piksellere çevir
                shares[0][i, j] = random.choice([bit1, 1 - bit1]) * 255
                shares[1][i, j] = random.choice([bit2, 1 - bit2]) * 255
                shares[2][i, j] = random.choice([bit3, 1 - bit3]) * 255
            else:  # Beyaz piksel
                # Beyaz piksel için paylar rastgele olmalı ama XOR ile doğru çıkmalı
                bit1 = random.randint(0, 1)
                bit2 = random.randint(0, 1)
                bit3 = bit1 ^ bit2  # XOR işlemi

                shares[0][i, j] = bit1 * 255
                shares[1][i, j] = bit2 * 255
                shares[2][i, j] = bit3 * 255
    return shares

def combine_shares_3_3(shares):
    """
    Üç payı birleştirerek orijinal görüntüyü geri oluşturur.
    XOR işlemi kullanılır.
    """
    combined = np.bitwise_xor(np.bitwise_xor(shares[0], shares[1]), shares[2])
    return combined

# Ana program
if __name__ == "__main__":
    # Giriş görüntüsünü yükle ve siyah-beyaz (binary) yap
    image_path = 'image.png'  # Görüntü yolu
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        print("Resim yüklenemedi! Dosya yolunu kontrol edin.")
        exit()

    # Görüntüyü siyah-beyaz formata dönüştür
    _, img_binary = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)

    # (3,3) payları oluştur
    shares = create_shares_3_3(img_binary)

    # Payları kaydet
    for idx, share in enumerate(shares):
        cv2.imwrite(f"share_{idx+1}.png", share)

    print("Paylar başarıyla oluşturuldu ve kaydedildi.")

    # Payları birleştir ve sonucu göster
    combined_image = combine_shares_3_3(shares)
    cv2.imwrite("combined.png", combined_image)

    # Payları ve birleşmiş görüntüyü göster
    for idx, share in enumerate(shares):
        cv2.imshow(f"Share {idx+1}", share)
    cv2.imshow("Combined Image", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
