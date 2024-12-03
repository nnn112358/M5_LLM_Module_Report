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

ユーザを作成します。

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

ユーザをsudoグループに追加します。

```
root@m5stack-LLM:~# gpasswd -a user_name sudo
Adding user user_name to group sudo
```

Sambaをインストールします。

```
root@m5stack-LLM:~# sudo apt install -y samba
```

Sambaの設定ファイルをバックアップします。
```
root@m5stack-LLM:~# cd /etc/samba/
root@m5stack-LLM:~# sudo cp -a smb.conf smb.conf.default
```

```
  951  sudo vim smb.conf
```

smb.confの末尾に下記を追加します。

```smb.conf
[user_name]
path = /home/user_name/
browsable = yes
writable = yes
guest ok = no
read only = no
```

ユーザーにsambaパスワードを設定します。


```
root@m5stack-LLM:~# sudo smbpasswd -a user_name
New SMB password:
Retype new SMB password:
Added user user_name.
```

```
PCから、共有フォルダへアクセスして確認します。
\\｛samba接続先IPアドレス｝\｛ユーザー名｝
```

