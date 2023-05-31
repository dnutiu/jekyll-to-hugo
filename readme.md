# Jekyll to Hugo Converter

Jekyll to Hugo Converter is a simple tool to convert Jekyll posts to Hugo posts.

You can also use it to convert your WordPress blog into a Hugo blog. Tutorial coming soon.

Note:
- This tool is still under development.
- This tool is not perfect, it will not convert everything. If you find a bug, please open a PR.

## Usage

```bash
pip install -r requirements.txt
python3 jekyll-to-hugo.py <jekyll_post_path> <hugo_post_path>
```

To change the config, edit `config.yaml`.

The configuration file path can be configured with the `CONFIG_PATH` environment variable.

---
Made with ❤️ by [NucuLabs.dev](https://blog.nuculabs.dev)