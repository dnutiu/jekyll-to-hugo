# Jekyll to Hugo Converter

Jekyll to Hugo Converter is a simple tool to convert Jekyll posts to Hugo posts.

I've used this tool to convert [my blog](https://blog.nuculabs.dev) from WorPress to Jekyll to Hugo.

Note: This tool is not perfect, it will not convert everything. If you find a bug, please open a PR.

## Table of Contents

* [Usage](#usage)
  * [PiPy](#pipy)
  * [Python From Source](#python-from-source)
  * [Docker](#docker)
* [Configuration](#configuration)
* [License](#license)

## Usage

### PiPy or Pipx

If you have Python installed, you can use the following commands:

```bash
pip install jekyll-to-hugo
jekyll-to-hugo
```

You will need to create a `config.yaml` file in the current directory. See example [here](./config.yaml).

_`pipx` is a tool to install Python CLI tools in isolated environments_

### Python From Source

If you have Python installed, you can use the following commands:

```bash
pip install -r requirements.txt
python3 jekyll-to-hugo.py <jekyll_post_path> <hugo_post_path>
```

To change the config, edit `config.yaml`.

The configuration file path can be configured with the `CONFIG_PATH` environment variable.

### Docker

If you don't have Python installed, you can use Docker:

1. Build the image.

```bash
docker build -t jekyll-to-hugo .
```

2. Run the image. You will need to mount the following directories: config file, Jekyll posts directory, Hugo posts directory.

```bash
docker run -it --rm -v $(pwd):/app jekyll-to-hugo
```

## Configuration

The configuration file is a YAML file. See example [here](./config.yaml).
The configuration file path can be configured with the `CONFIG_PATH` environment variable.

## License

This project is licensed under the GPL-3.0 license - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ by [NucuLabs.dev](https://blog.nuculabs.dev)