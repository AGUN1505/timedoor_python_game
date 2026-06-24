# Mengimpor modul Pygame untuk membuat game dan menangani grafik serta input
import pygame
# Modul sys untuk fungsi level sistem seperti keluar dari program
import sys
# Modul random untuk menghasilkan posisi apel secara acak
import random
# Modul time untuk delay/sleep (digunakan saat game over)
import time

# Inisialisasi Pygame (mengembalikan tuple status yang disimpan di check_errors)
check_errors = pygame.init()
# Lebar jendela game (piksel)
frame_size_x = 720
# Tinggi jendela game (piksel)
frame_size_y = 480
# Menetapkan judul jendela
pygame.display.set_caption('Snake Game')
# Membuat surface jendela dengan ukuran yang telah ditentukan
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
# Clock untuk mengontrol frame rate/kecepatan game loop
fps_controller = pygame.time.Clock()
# Arah awal pergerakan ular (string)
direction = 'RIGHT'
# Variabel penampung perubahan arah dari input sebelum divalidasi
change_to = direction

# Skor awal
score = 0

# Posisi kepala ular sebagai [x, y]
snake_pos = [100,50]
# List yang merepresentasikan tubuh ular; tiap elemen adalah [x, y]
snake_body = [[100,50],[90,50],[80,50]]
# Posisi apel di-generate acak pada grid yang merupakan kelipatan 10
apple_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
# Flag apakah apel saat ini muncul
apple_spawn = True

# Warna-warna yang digunakan (RGB)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)  # Tidak dipakai, tetapi didefinisikan


def game_over():
    # Membuat font besar untuk menampilkan pesan game over
    my_font = pygame.font.SysFont('Arial', 90)
    # Merender teks 'YOU DIED' berwarna merah
    game_over_surface = my_font.render('YOU DIED', True, red)
    # Mendapatkan rectangle dari surface teks untuk pengaturan posisi
    game_over_rect = game_over_surface.get_rect()
    # Menempatkan titik tengah atas teks di koordinat (360, 120)
    game_over_rect.midtop = (360, 120)
    # Mengisi layar dengan hitam sebelum menampilkan pesan
    game_window.fill(black)
    # Menggambar surface teks ke jendela pada posisi yang sudah ditentukan
    game_window.blit(game_over_surface, game_over_rect)
    # Memperbarui layar agar teks tampil
    pygame.display.flip()
    # Menunggu 3 detik agar pemain melihat pesan
    time.sleep(3)
    # Membersihkan Pygame
    pygame.quit()
    # Keluar dari program
    sys.exit()


# Loop utama game
while True:
    # Mengambil semua event dari queue Pygame
    for event in pygame.event.get():
        # Jika event tipe QUIT (mis. klik tombol close)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Jika ada event tombol ditekan
        elif event.type == pygame.KEYDOWN:
            # Jika tombol panah atas ditekan, set change_to menjadi 'UP'
            if event.key == pygame.K_UP :
                change_to = 'UP'
            # Jika tombol panah bawah ditekan
            if event.key == pygame.K_DOWN :
                change_to = 'DOWN'
            # Jika tombol panah kiri ditekan
            if event.key == pygame.K_LEFT :
                change_to = 'LEFT'
            # Jika tombol panah kanan ditekan
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            # Jika ESC ditekan, kirim event QUIT untuk keluar program
            if event.key == pygame.K_ESCAPE:
               pygame.event.post(pygame.event.Event(pygame.QUIT))
               
    # Validasi perubahan arah: mencegah balik 180 derajat
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
        
    # Perbarui posisi kepala ular berdasarkan arah saat ini (grid 10 piksel)
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
        
    # Mengisi background frame saat ini dengan warna putih
    game_window.fill(white)
    # Debug: mencetak nilai change_to di konsol (boleh dihapus)
    print(change_to)
    # Masukkan posisi kepala baru ke awal list tubuh (bergerak maju)
    snake_body.insert(0, list(snake_pos))
    
    # Jika kepala berada di posisi apel, tambahkan skor dan tandai agar apel di-respawn
    if snake_pos[0] == apple_pos[0] and snake_pos[1] == apple_pos[1]:
        score += 1
        apple_spawn = False
    else:
        # Jika tidak makan apel, hapus segmen terakhir tubuh (agar panjang tetap)
        snake_body.pop()
        
    # Gambar setiap segmen ular sebagai kotak 10x10 berwarna hijau
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    # Jika apel tidak ada, buat posisi baru secara acak
    if not apple_spawn:
        apple_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    # Tandai apel sekarang muncul (baik baru atau sebelumnya)
    apple_spawn = True
    # Gambar apel sebagai kotak 10x10 berwarna merah
    pygame.draw.rect(game_window, red, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))
    
    # Cek apakah kepala keluar batas layar (kiri/kanan)
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    # Cek apakah kepala keluar batas layar (atas/bawah)
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
        
    # Cek tabrakan kepala dengan tubuh (skip kepala sendiri di index 0)
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
    
    # Menampilkan skor di layar menggunakan font kecil
    score_font = pygame.font.SysFont('Arial', 20)
    score_surface = score_font.render('Score : ' + str(score), True, black)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (72, 15)
    game_window.blit(score_surface, score_rect)
    
    # Perbarui tampilan dan batasi frame rate
    pygame.display.update()
    fps_controller.tick(10)