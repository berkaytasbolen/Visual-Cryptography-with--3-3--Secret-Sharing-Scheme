import cv2
import numpy as np
import random

def create_shares_3_3(img_binary):
    h, w = img_binary.shape
    shares = [np.zeros((h, w), dtype=np.uint8) for _ in range(3)]

    for i in range(h):
        for j in range(w):
            pixel = img_binary[i, j]
            if pixel == 0:  # Siyah piksel (gizli)
                patterns = [
                    [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],  # Rastgele desen 1
                    [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)],  # Rastgele desen 2
                    [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]   # Rastgele desen 3
                ]
            else:  # Beyaz piksel (gizli değil)
                patterns = [
                    random.sample([0, 1, 1], 3),  # %67 beyaz
                    random.sample([0, 1, 1], 3),  # %67 beyaz
                    random.sample([0, 1, 1], 3)   # %67 beyaz
                ]

            for k in range(3):
                shares[k][i, j] = patterns[k][k] * 255  # Her paya farklı desen ata

    return shares

def combine_shares_3_3(shares):
    combined = np.zeros_like(shares[0])

    for i in range(3):
        combined = np.bitwise_or(combined, shares[i])
    
    return combined

if __name__ == "__main__":
    image_path = 'image.png'
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img_gray is None:
        print("Resim yuklenemedi! Dosya yolunu kontrol edin.")
        exit()

    _, img_binary = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
    shares = create_shares_3_3(img_binary)

    for idx, share in enumerate(shares):
        cv2.imwrite(f"share_{idx+1}.png", share)

    print("Paylar basariyla olusturuldu ve kaydedildi.")

    combined_image = combine_shares_3_3(shares)
    cv2.imwrite("combined.png", combined_image)

    for idx, share in enumerate(shares):
        cv2.imshow(f"Share {idx+1}", share)
    cv2.imshow("Combined Image", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
