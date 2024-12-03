## 目的
Module-LLMとPCとの間でファイルをコピーする手段について。


## SCPでファイル転送

### PC→Module-LLMへSCPでファイル転送①

TeraTermから、SSH接続でModule-LLMと通信をしている場合、TeraTermのGUIからSCPコマンド使うことができます。 <br>
SCPはリモートマシンとローカルマシンとの間でファイルをコピーする際に使用するLinuxのコマンドですが、TeraTermはGUIにSCPの機能を設けています。

TeraTermのウィンドウへ、PC内の転送したいファイルをドラッグ＆ドロップします。 <br>
SCPのWindowが出てきますので、転送先のModule-LLMのフォルダのパスを入力してOKを押します。 <br>
<img src="https://github.com/user-attachments/assets/aa4324be-f677-4772-9a42-f06eaa35eaa5" width="50%">


### PC→Module-LLMへSCPでファイル転送②
メニューのファイルから、SSH SCPを選択します。 <br>
<img src="https://github.com/user-attachments/assets/92fa47e2-0f47-45e4-8e28-ae59a9690868" width="50%">


SCPのウィンドウの上半分のメニューを使います。PC内のファイルを選択、もしくはPC内のファイルをこのウィンドウにドラックし、転送先のModule-LLMのフォルダのパスを入力して送信を押します。 <br>
<img src="https://github.com/user-attachments/assets/f702efaa-1f78-4078-a60b-59de5f37cc41" width="50%">

### Module-LLM→PCへSCPでファイル転送

SCPのウィンドウの下半分のメニューを使います。Module-LLM内のファイルのパスを入力し、転送先のPCのフォルダのパスを入力して受信を押します。 <br>

<img src="https://github.com/user-attachments/assets/3241c6b9-57a4-4b95-8f83-e35b6c28e798" width="50%">


## Module-LLMにSambaをインストールする。

Module-LLMのRootアカウントへ、デバック基板からログインをします。

Sambaで使用する専用ユーザーアカウントを作成します。以下のコマンドでユーザーを作成します。
パスワードの設定は必須ですが、その他の情報（フルネーム、部屋番号、電話番号など）は任意です。

```
root@m5stack-LLM:~# adduser user_name
Adding user `user_name' ...
Adding new group `user_name' (1001) ...
Adding new user `user_name' (1001) with group `user_name' ...
Creating home directory `/home/user_name' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for user_name
Enter the new value, or press ENTER for the default
        Full Name []:
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n]
```

作成したユーザーに管理者権限を付与するため、sudoグループに追加します。

```
root@m5stack-LLM:~# gpasswd -a user_name sudo
Adding user user_name to group sudo
```

次に、Sambaパッケージのインストールを行います。Ubuntuのパッケージマネージャーを使用して、以下のコマンドでインストールします。

```
root@m5stack-LLM:~# sudo apt install -y samba
```

インストール完了後、Sambaの設定ファイルを編集する前に、現在の設定をバックアップします。
これは、設定に問題が発生した場合に元の状態に戻せるようにするためです。

```
root@m5stack-LLM:~# cd /etc/samba/
root@m5stack-LLM:~# sudo cp -a smb.conf smb.conf.default
```

次に、Samba設定ファイルを編集します。このファイルには、共有の基本設定からセキュリティ設定まで、重要な設定が含まれます：
```
  951  sudo vim smb.conf
```

ユーザー専用の共有設定を追加します。この設定により、指定したユーザーのみがアクセスできる共有フォルダを作成することができます。

```smb.conf
[user_name]
path = /home/user_name/
browsable = yes
writable = yes
guest ok = no
read only = no

各設定項目の説明：
path: 共有するディレクトリのパス
valid users: アクセスを許可するユーザーを指定
browsable: 共有フォルダの表示・非表示
writable: 書き込み権限の有無
guest ok: ゲストアクセスの許可
create mask: 新規作成ファイルのパーミッション
directory mask: 新規作成ディレクトリのパーミッション
force user/group: アクセス時の強制ユーザー/グループ
```

設定が完了したら、Sambaユーザーのパスワードを設定します。このパスワードは、Windowsからアクセスする際に使用されます。

```
root@m5stack-LLM:~# sudo smbpasswd -a user_name
New SMB password:
Retype new SMB password:
Added user user_name.
```
すべての設定が完了したら、Sambaサービスを再起動して新しい設定を適用します：

```
sudo systemctl restart smbd
sudo systemctl restart nmbd
```
PCから、共有フォルダへアクセスして確認します。
Windowsのエクスプローラーのアドレスバーに以下の形式でアドレスを入力します。
接続時に認証ダイアログが表示されますので、設定したSambaユーザー名とパスワードを入力してアクセスします。

```
\\｛samba接続先IPアドレス｝\｛ユーザー名｝
```

