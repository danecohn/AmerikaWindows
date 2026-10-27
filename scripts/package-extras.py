"""Additional installers; leaves the six existing artifact names and data paths intact."""
from pathlib import Path
import hashlib,json,os,platform,shutil,subprocess,sys,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
ARCH={'aarch64':'arm64','arm64':'arm64','x86_64':'x64','amd64':'x64'}[platform.machine().lower()]
RELEASE=ROOT/'release';SOURCE=ROOT/'dist/AltStackSocial';TOOLS=ROOT/'build/installer-tools';TOOLS.mkdir(parents=True,exist_ok=True)
LOCK=json.loads((ROOT/'packaging/toolchain.json').read_text())
def download(key):
    spec=LOCK[key];path=TOOLS/spec['file']
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=spec['sha256']:
        with urllib.request.urlopen(spec['url'],timeout=120) as response,path.open('wb') as output:shutil.copyfileobj(response,output)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=spec['sha256']:raise RuntimeError('Installer tool checksum mismatch: '+key)
    return path
if sys.platform=='win32':
    archive=download('nsis')
    with zipfile.ZipFile(archive) as z:z.extractall(TOOLS)
    compiler=next(TOOLS.glob('nsis-*/makensis.exe'))
    manifest=TOOLS/'remove-owned-files.nsh'
    def escaped(path):return str(path).replace('$','$$').replace('"','$\\"')
    commands=['Delete "$INSTDIR\\'+escaped(p.relative_to(SOURCE))+'"' for p in SOURCE.rglob('*') if p.is_file()]
    commands+=['RMDir "$INSTDIR\\'+escaped(p.relative_to(SOURCE))+'"' for p in sorted(SOURCE.rglob('*'),key=lambda p:len(p.parts),reverse=True) if p.is_dir()]
    manifest.write_text('\n'.join(commands)+'\n',encoding='utf-8')
    output=RELEASE/f'AltStackSocial-windows-{ARCH}-setup.exe'
    subprocess.run([str(compiler),'/DREPO='+str(ROOT),'/DSOURCE='+str(SOURCE),'/DOUTPUT='+str(output),'/DREMOVAL_MANIFEST='+str(manifest),str(ROOT/'packaging/social.nsi')],check=True)
elif sys.platform.startswith('linux'):
    appdir=TOOLS/'AppDir';appdir.mkdir(exist_ok=True)
    shutil.copytree(SOURCE,appdir/'AltStackSocial',dirs_exist_ok=True)
    shutil.copy2(ROOT/'assets/logo.png',appdir/'altstack-social.png')
    shutil.copy2(ROOT/'assets/logo.png',appdir/'.DirIcon')
    desktop=(ROOT/'packaging/amerika-social.desktop').read_text().replace('Exec=AltStackSocial','Exec=AppRun')
    (appdir/'altstack-social.desktop').write_text(desktop)
    (appdir/'AppRun').write_text('#!/bin/sh\nset -eu\nHERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)\nexec "$HERE/AltStackSocial/AltStackSocial" "$@"\n')
    (appdir/'AppRun').chmod(0o755)
    tool=download('appimage-'+ARCH);tool.chmod(0o755)
    subprocess.run([str(tool),str(appdir),str(RELEASE/f'AltStackSocial-linux-{ARCH}.AppImage')],check=True,env={**os.environ,'ARCH':'aarch64' if ARCH=='arm64' else 'x86_64','APPIMAGE_EXTRACT_AND_RUN':'1'})
    stage=TOOLS/'deb';(stage/'DEBIAN').mkdir(parents=True,exist_ok=True)
    shutil.copytree(SOURCE,stage/'opt/altstack-social',dirs_exist_ok=True)
    (stage/'usr/bin').mkdir(parents=True,exist_ok=True)
    (stage/'usr/bin/altstack-social').write_text('#!/bin/sh\nexec /opt/altstack-social/AltStackSocial "$@"\n');(stage/'usr/bin/altstack-social').chmod(0o755)
    (stage/'usr/share/applications').mkdir(parents=True,exist_ok=True)
    (stage/'usr/share/applications/altstack-social.desktop').write_text((ROOT/'packaging/amerika-social.desktop').read_text().replace('Exec=AltStackSocial','Exec=/usr/bin/altstack-social'))
    icons=stage/'usr/share/icons/hicolor/512x512/apps';icons.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'assets/logo.png',icons/'altstack-social.png')
    docs=stage/'usr/share/doc/altstack-social';docs.mkdir(parents=True,exist_ok=True)
    for name in ['LICENSE','THIRD-PARTY-NOTICES.md']:shutil.copy2(ROOT/name,docs/name)
    (stage/'DEBIAN/control').write_text('Package: altstack-social\nVersion: 1.3.2\nArchitecture: '+('arm64' if ARCH=='arm64' else 'amd64')+'\nMaintainer: VigilTech\nSection: net\nPriority: optional\nDepends: libc6 (>= 2.39), libgl1, libegl1, libxcb-cursor0, libxkbcommon-x11-0, libdbus-1-3, libsecret-1-0\nDescription: Vigil Social native desktop client\n Native Qt application by VigilTech.\n')
    subprocess.run(['dpkg-deb','--root-owner-group','--build',str(stage),str(RELEASE/f'AltStackSocial-linux-{ARCH}.deb')],check=True)
else:raise SystemExit('Additional packaging is for Windows and Linux only.')
for p in RELEASE.iterdir():
    if p.suffix in ('.exe','.AppImage','.deb'):p.with_name(p.name+'.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
