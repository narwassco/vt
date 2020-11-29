import os
import argparse
from OpenAfricaUploader import OpanAfricaUploader

def get_args():
  prog = "upload2openafrica.py"
  usage = "%(prog)s [options]"
  parser = argparse.ArgumentParser(prog=prog, usage=usage)
  parser.add_argument("--key", dest="key", help="Your CKAN api key", required=True)
  parser.add_argument("--org", dest="organization", help="Your organization name", required=True)
  parser.add_argument("--pkg", dest="package", help="Target url of your package", required=True)
  parser.add_argument("--title", dest="title", help="Title of your package", required=True)
  parser.add_argument("--file", dest="file", help="Relative path of file which you would like to upload", required=True)
  parser.add_argument("--desc", dest="description", help="any description for your file", required=True)
  args = parser.parse_args()

  return args

if __name__ == "__main__":
  args = get_args()

  uploader = OpanAfricaUploader(args.key)
  uploader.create_package(args.organization, args.package,args.title)
  uploader.upload_datasets(os.path.abspath(args.file), args.description)
