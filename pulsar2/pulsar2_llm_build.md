# Large Model Compilation (Experimental Stage)

この文書は、Axera Technology社の大規模言語モデル（LLM）コンパイル実験についての技術ガイドです。主な内容を要約します：

# Large Model Compilation（実験段階）

## サポートされているプラットフォーム
- AX650N
- AX630C

## 検証済みモデル
以下のようなモデルが対象となっています：
- Llama2、Llama3、Llama3.2
- TinyLlama-1.1B
- Qwen1.5、Qwen2、Qwen2.5
- Phi2、Phi3
- MiniCPM、MiniCPM-V 2.0
- SmolLM
- ChatGLM3
- OpenBuddy

## 主な目的
HuggingFaceからダウンロードしたモデル（*.safetensor または pytorch_model.bin）を、Pulsar2ツールを使用して`axmodel`に変換する方法を説明しています。

## モデル変換の基本手順

1. モデルをダウンロード
2. `pulsar2 llm_build`コマンドでモデルを変換
3. 埋め込みファイルを抽出・最適化
4. 変換されたモデルファイルを開発ボードで実行

## 具体的な例：Qwen2-0.5B-Instructモデル

### ダウンロードコマンド
```shell
huggingface-cli download --resume-download Qwen/Qwen2-0.5B-Instruct
```

### モデル変換コマンド
```shell
pulsar2 llm_build --input_path Qwen/Qwen2-0.5B-Instruct/ --output_path Qwen/Qwen2-0.5B-w8a16/ --kv_cache_len 1023 --hidden_state_type bf16 --prefill_len 128 --chip AX650
```

## デバッグ方法

Pulsar2には2つのデバッグレベルがあります：

1. `--check_level 1`: 最初の層の類似性をテスト
2. `--check_level 2`: プロンプト入力を指定してモデルファイルをシミュレーション

## 追加の例：MiniCPM-V 2.0

ドキュメントでは、MiniCPM-V 2.0モデルの変換と実行についても詳細な手順を提供しています。

## トークナイザーについて

トークナイザーはローカルモジュールとHTTPサーバーの両方を使用できます。sentencepieceの代わりに、transformersライブラリのAutoTokenizerモジュールを直接呼び出すHTTPサーバー方式を推奨しています。

## 関連プロジェクト

- [AX-LLM GitHub Project](https://github.com/AXERA-TECH/ax-llm)

このガイドは、Axera Technology社の開発ボード上で大規模言語モデルをコンパイルし、実行するための包括的な手順を提供しています。


4.5.2. トークナイザーパーサーの説明

ax-llmプロジェクトのトークナイザーパーサーは、ローカルモジュールとHTTPサーバーの両方を使用しています。ローカルソリューションでは、sentencepieceとtiktokenの2つの方式を試してきました。

しかし、実際のデバッグ中に、sentencepieceは異なるLLMモデルの特殊トークンをうまくサポートできないことが分かりました。ユーザーは特殊トークンの分割を自分で処理する必要があり、これにより開発ボード上のトークンIDとtransformersライブラリのAutoTokenizerモジュールから取得したトークンIDに差異が生じやすく、最終的にLLMの出力結果の正確性に影響を与える可能性があります。

そのため、初期デバッグではtransformersライブラリのAutoTokenizerモジュールを直接呼び出すトークナイザーHTTPサーバー方式を推奨しています。

トークナイザーHTTPサーバーの特徴:
* 正確なトークンIDを保証
* チャットテンプレートの追加を容易に
* ローカルおよびリモートデプロイをサポート
* 複数ユーザーのアクセスをサポート

ネットディスク上のQwen2.5 3B用の提供ファイルの例:

```
root@xxx:/data/ax-llm-build# tree qwen2.5-3b-prefill-ax650/
qwen2.5-3b-prefill-ax650/
├── main_prefill
├── qwen2.5-3B-prefill-ax650
│   ├── model.embed_tokens.weight.bfloat16.bin
│   ├── qwen2_p128_l0_together.axmodel
    ...
│   ├── qwen2_p128_l12_together.axmodel
│   └── qwen2_post.axmodel
├── qwen2.5_tokenizer
│   ├── merges.txt
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   └── vocab.json
├── qwen2.5_tokenizer.py
├── qwen.tiktoken
├── readme.txt
└── run_qwen2.5_3B_prefill_ax650.sh
```

* qwen2.5_tokenizer: Qwen/Qwen2.5-3B-Instructから抽出されたトークナイザー関連ファイル
* qwen2.5_tokenizer.py: Pythonで実装されたトークナイザーHTTPサーバー

実行手順は以下の通り:
* python qwen2.5_tokenizer.py --host xxx.xxx.xxx.xxx --port 12345。ここで--host xxx.xxx.xxx.xxxはトークナイザー解析サーバーのIPアドレスを設定します。AX650Nがこのアドレスに適切にアクセスできることを確認してください。Pythons環境があるAX650N上でネイティブに実行できます。
* run_qwen2.5_3B_prefill_ax650.shの--filename_tokenizer_modelのIPアドレスをステップ1と同じものに変更します。
* run_qwen2.5_3B_prefill_ax650.shを実行します。

```
root@xxx:/data/ax-llm-build# cat qwen2.5-3b-prefill-ax650/run_qwen2.5_3B_prefill_ax650.sh
./main_prefill \
--template_filename_axmodel "qwen2.5-3B-prefill-ax650/qwen2_p128_l%d_together.axmodel" \
--axmodel_num 36 \
--tokenizer_type 2 \
--filename_tokenizer_model http://xxx.xxx.xxx.xxx:12345 \
--bos 0 --eos 0 \
--filename_post_axmodel "qwen2.5-3B-prefill-ax650/qwen2_post.axmodel" \
--filename_tokens_embed "qwen2.5-3B-prefill-ax650/model.embed_tokens.weight.bfloat16.bin" \
--tokens_embed_num 151936 \
--tokens_embed_size 2048 \
--use_mmap_load_embed 1 \
--live_print 1 \
--continue 1 \
--prompt "$1"
```
