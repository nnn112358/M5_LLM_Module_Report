
## dockerのインストール

dockerをインストールします。<br>
Ubuntu 22.04にDockerをインストールするには、古いバージョンを削除し、必要なパッケージをインストールしてからDockerの公式GPGキーとリポジトリを追加し、Docker EngineとCompose pluginをインストール後、ユーザーをdockerグループに追加します。<br>

```
# 古いバージョンを削除
sudo apt-get remove docker docker-engine docker.io containerd runc

# 必要なパッケージをインストール
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Dockerの公式GPGキーを追加
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# リポジトリを設定
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Dockerエンジンをインストール
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# ユーザーをdockerグループに追加（再ログイン必要）
sudo usermod -aG docker $USER

# Dockerデーモンが起動していることを確認
sudo systemctl status docker
```

 インストール後はdocker run hello-worldで動作確認できます。
```
docker --version
docker run hello-world
```

## pulsar2のインストール

Axera-Techの@qqc-sanが管理するGoogleDriveからax_pulsar2_3.2_patch1_temp_vlm.tar.gzをダウンロードしてきます。
<https://drive.google.com/drive/folders/10rfQIAm5ktjJ1bRMsHbUanbAplIn3ium>

以下のコマンドでdockerを読み込みます。

```
sudo docker load -i ax_pulsar2_3.2_patch1_temp_vlm.tar.gz
```
Dockerイメージを確認します。
```
$ sudo docker image ls
REPOSITORY                  TAG             IMAGE ID       CREATED         SIZE
pulsar2                     3.2             9a6b9d26f6a1   2 months ago    2.58GB
pulsar2                     temp-58aa62e4   c6ccb211d0bc   4 weeks ago     2.58GB
```

Dockerを起動します。

```
 sudo docker run -it --net host --rm -v $PWD:/data pulsar2:3.2
 ```





# 参考

https://pulsar2-docs.readthedocs.io/en/latest/index.html
