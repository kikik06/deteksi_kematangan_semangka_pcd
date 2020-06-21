# import library numpy untuk mempermudah komputasi saintifik
import numpy as np
# dari Python Image Library (PIL) import ImageTk dan Image
from PIL import ImageTk, Image
# dari matplotlib.figure import Figure untuk membuat visualisasi
from matplotlib.figure import Figure
# library untuk menampilkan visualisasi di GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# tkinter adalah libary GUI untuk python
from tkinter import Tk, Button, filedialog, Label, Canvas, Message

# deklarasi panel untuk menampilkan foto original, foto hitam putih 
# histogram dan pesan teks hasil deteksi
panel_photo = None
panel_photo_bw = None
panel_histogram_gs =  None
panel_message = None
# fungsi untuk membuka, menampilkan citra original, 
# menampilkan foto hitam putih, histogram dan melakukan deteksi
def process_img():
    # panjang citra di GUI
    width = 240
    # lebar citra di GUI
    height = 240
    # mendeklarasikan panel yang sudah dideklarasikan menjadi global
    global panel_photo, panel_photo_bw, panel_histogram_gs, panel_message
    # jika fungsi process_img() sudah dijalankan sebelumnya
    # maka tutup / hapus panel yang sudah ada sebelumnya
    if panel_photo != None:
        panel_photo.destroy()
        panel_photo_bw.destroy()
        panel_histogram_gs.get_tk_widget().destroy()
        panel_message.destroy()
    
    # tampilkan jendela untuk memilih file citra yang akan diproses
    file_name = filedialog.askopenfilename(title ='Select Image')
    # simpan file sebagai citra
    img = Image.open(file_name)
    # ubah ukuran citra sesuai panjang dan lebar yg telah ditentukan
    img_resized = img.resize((width, height), Image.ANTIALIAS)
    # ubah citra menjadi citra untuk GUI
    img_tk = ImageTk.PhotoImage(img_resized)
    # tampilkan citra di panel_photo dengan posisi x=10 dan y=50
    panel_photo = Canvas(root)
    panel_photo.place(x=10, y=50)
    # posisikan citra di dalam panel photo di x=0, y=0
    # dan terletak di northwest(kiri atas)
    panel_photo.create_image(0, 0, anchor='nw', image=img_tk)
    panel_photo.image = img_tk
    
    # threshold untuk mengubah citra abu - abu menjadi hitam putih umumnya 128
    # nilai threshold tidaklah mutlak 128
    # untuk menyesuaikan dengan output yang paper referensi maka threshold kita ubah menjadi 60
    # citra diubah menjadi hitam putih agar dapat menampilkan garis semangka
    threshold = 60
    # ubah citra dari RGBA ke abu - abu
    img_gs = img_resized.convert('L')
    # ubah citra dari abu - abu ke hitam putih
    img_bw = img_gs.point(lambda p: 255 if p > threshold else 0, mode='1')
    # ubah citra hitam putih menjadi citra untuk GUI
    img_bw_tk = ImageTk.PhotoImage(img_bw)
    # tampilkan citra di panel_photo_bw dengan posisi x=260 dan y=50
    panel_photo_bw = Canvas(root)
    panel_photo_bw.place(x=260, y=50)
    # posisikan citra di dalam panel photo di x=0, y=0
    # dan terletak di northwest(kiri atas)
    panel_photo_bw.create_image(0, 0, anchor='nw', image=img_bw_tk)
    panel_photo_bw.image = img_bw_tk

    # ambil seluruh representasi derajat keabuan citra pada tiap piksel
    # lalu jadikan sebagai array
    a = np.array(img_gs.getdata())
    # buat Figure / visualisasi dengan panjang=5, lebar=4 dan 100 dot per inch
    f = Figure(figsize=(5,4), dpi=100)
    # buat Figure / visualisasi dapat ditampilkan di GUI
    panel_histogram_gs = FigureCanvasTkAgg(f, root)
    # posisikan visualisasi di x=510 dan y=10
    panel_histogram_gs.get_tk_widget().place(x=510, y=10)
    # ambil instance axis milik figure lalu assign ke variabel p
    p = f.gca()
    # buat histogram dengan isi array a dan bins=[0,...,255]
    p.hist(a, bins=range(256))

    # deklarasi variabel total dan threshold atas bawah untuk r,g,b
    # threshold ini menentukan apakah semangka matang berdasar nilai rgbnya
    total = 0
    red_lower_threshold = 92
    red_upper_threshold = 100
    green_lower_threshold = 170
    green_upper_threshold = 210
    blue_lower_threshold = 0
    blue_upper_threshold = 90
    # ubah citra dari RGBA menjadi RBG lalu ambil total kemunculan RGB dan nilai RGBnya
    list_count_rgb = img_resized.convert('RGB').getcolors(width * height)
    # loop untuk tiap anggota list
    for count_rgb in list_count_rgb:
        # cek nilai merah, jika berada di dalam threshold maka
        # total += total kemunculan rgb
        if count_rgb[1][0] >= red_lower_threshold and \
            count_rgb[1][0] <= red_upper_threshold:
            total += count_rgb[0]
        # cek nilai hijau, jika berada di dalam threshold maka
        # total += total kemunculan rgb
        if count_rgb[1][1] >= green_lower_threshold and \
            count_rgb[1][1] <= green_upper_threshold:
            total += count_rgb[0]
        # cek nilai biru, jika berada di dalam threshold maka
        # total += total kemunculan rgb
        if count_rgb[1][2] >= blue_lower_threshold and \
            count_rgb[1][2] <= blue_upper_threshold:
            total += count_rgb[0]
    # hitung persentase kematangan berdasarkan nilai rgb
    ripe_percentage = (total / (3 * width * height)) * 100
    # deklarasi pesan
    message = 'Belum Matang'
    # jika persentase kematangan >= 25 maka matang
    # (berdasarkan training dari percobaan yg ada)
    if ripe_percentage >= 25:
        message = 'Matang'
    # deklarasi panel_message untuk menampilkan pesan status semangka 
    panel_message = Message(root, text='Status Semangka: {}'.format(message))
    # tampilkan pesan di x=10, y=300
    panel_message.place(x=10, y=300)

    # deklarasi panjang dan lebar untuk sample file csv
    width_sample = 30
    height_sample = 30
    # resize citra abu - abu sesuai panjang lebar sample
    img_gs_resized = img_gs.resize((width_sample, height_sample), Image.ANTIALIAS)
    # ambil derajat nilai keabuan tiap piksel
    pix_gs_resized = img_gs_resized.load()
    # tulis derajat nilai keabuan tiap piksel ke file csv
    with open('gs_pixel.csv', 'w+') as f:
        for x in range(width_sample):
            for y in range(height_sample):
                gs_val = pix_gs_resized[y,x]
                f.write('{},'.format(gs_val))
            f.write('\n')
    # resize citra hitam putih sesuai panjang lebar sample
    img_bw_resized = img_bw.resize((width_sample, height_sample), Image.ANTIALIAS)
    # ambil derajat nilai hitam putih tiap piksel
    pix_bw_resized = img_bw_resized.load()
    # tulis derajat nilai keabuan tiap piksel ke file csv
    with open('bw_pixel.csv', 'w+') as f:
        # read the details of each pixel and write them to the file
        for x in range(width_sample):
            for y in range(height_sample):
                bw_val = pix_bw_resized[y,x]
                # karena derajat nilai hitam putih direpesentasikan dengan 0 dan 255
                # kita dapat mengubahnya menjadi 0 1 sebagai berikut
                if bw_val == 255:
                    bw_val = 1
                f.write('{},'.format(bw_val))
            f.write('\n')

# deklarasi GUI
root = Tk()
# deklarasi judul GUI
root.title('Watermelon Ripeness Detection')
# deklarasi ukuran GUI
root.geometry('1000x450')
# deklarasi apakah GUI panjang lebar GUI bisa diubah ukurannya
root.resizable(width=True, height = True)
# deklarasi tombol untuk membuka gambar dan memprosesnya lalu letakkan di x=0, y=0
btn = Button(root, text ='Open & Process Image', command = process_img).place(x=0, y=0)
# tampilkan GUI secara terus menerus selama tidak ditutup
root.mainloop()