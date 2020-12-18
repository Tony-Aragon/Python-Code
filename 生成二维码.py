import qrcode
img = qrcode.make('https://github.com/Tony-Aragon/Python-Code')
img.save('Mygithub.jpg')
img.show()