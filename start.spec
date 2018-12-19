# -*- mode: python -*-

block_cipher = None


a = Analysis(['start.py'],
             pathex=['E:\\WorkPlace\\YarlungSoftware\\python\\RemoteOperation2'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas +=[('Res\\cc.png','Res\\cc.png','DATA'),('Res\\private.pem','Res\\private.pem','DATA'),('Res\\public.pem','Res\\public.pem','DATA')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='start',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='Res\\ico.ico')
