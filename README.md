# ctfh
Cloudformation Template For Humans

Install libjpeg-dev
```bash
sudo apt-get install zlib1g-dev libjpeg-dev libpng-dev python-dev
```

I used imagemagick to display resulted images
```bash
sudo apt-get install imagemagick
display <filepath>
```

Install blockdiag (using a virtualenv is recommended)
```bash
pip install funcparserlib Pillow blockdiag boto
```

Usage:
```bash
python ctfh.py test.json > test.diag
```

This will create `test.png`

To create a cloudformation template for IAM infrastructure use `getiam.py`
Make sure you have your aws credentials exported to environment variables:
```bash
export EC2_ACCESS_KEY=yourawsaccesskey
export EC2_SECRET_KEY=yourawssecretkey
export EC2_REGION=yourawsregion
```